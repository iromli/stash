<?php
/**
 * Reflextor - Reflection extractor
 *
 * @author      Isman Firmansyah
 * @copyright   2011 Isman Firmansyah
 * @link        https://github.com/iromli/reflextor
 * @license     http://opensource.org/licenses/mit-license.php The MIT License
 */

namespace reflextor;

use \Exception;
use \reflextor\Builder;
use \reflextor\exception\IOException;

/**
 * Catches all uncaught exceptions.
 */
set_exception_handler(function(Exception $exception) {
    die($exception);
});

/**
 * Loader implementation that implements the technical interoperability
 * standards for PHP 5.3 namespaces and class names.
 *
 * @link http://groups.google.com/group/php-standards/web/psr-0-final-proposal
 */
spl_autoload_register(function($className) {
    $_namespace          = 'reflextor';
    $_namespaceSeparator = '\\';
    $_includePath        = dirname(__DIR__);

    $nsPath = substr($className, 0, strlen($_namespace . $_namespaceSeparator));

    if ($_namespace === null || $_namespace . $_namespaceSeparator === $nsPath) {
        $fileName  = '';
        $namespace = '';

        $lastNsPos = strripos($className, $_namespaceSeparator);
        if ($lastNsPos !== false) {
            $namespace = substr($className, 0, $lastNsPos);
            $className = substr($className, $lastNsPos + 1);
            $fileName  = str_replace($_namespaceSeparator, DIRECTORY_SEPARATOR, $namespace) . DIRECTORY_SEPARATOR;
        }

        $fileName .= str_replace('_', DIRECTORY_SEPARATOR, $className) . '.php';
        if ($_includePath !== null) {
            $fileName = $_includePath . DIRECTORY_SEPARATOR . $fileName;
        }

        require $fileName;
    }
});

/**
 * Bundle
 *
 * @package reflextor
 * @author Isman Firmansyah
 */
class Bundle {

    /**
     * Bundle's configuration.
     *
     * @var array
     * @access public
     */
    public $config = array();

    /**
     * Creates a new <tt>Bundle</tt>.
     *
     * Possible configuration values:
     * - <tt>name</tt>: Bundle name
     * - <tt>outputRoot</tt>: Absolute path to parent directory to store proposal files to
     *
     * @param array $config Configuration for current <tt>Bundle</tt> instance
     * @return void
     * @access public
     */
    public function __construct($config = array()) {
        $defaults = array(
            'name'       => 'php_internal',
            'outputRoot' => getenv('HOME') . DIRECTORY_SEPARATOR . '.reflextor' . DIRECTORY_SEPARATOR . 'bundles'
        );
        $this->config = (array)$config + $defaults;
    }

    /**
     * Creates directory and proposal files.
     *
     * @return boolean Whether bundle is successfully built or failed
     * @access public
     */
    public function build() {
        $builder = new Builder();

        $outputDir = $this->outputDir();
        if (file_exists($outputDir) === false) {
            if (@mkdir($outputDir, 0755, true) === false) {
                throw new IOException("Cannot create {$outputDir} directory -- Permission denied!");
            }
        }
        chmod($outputDir, 0755);

        $proposals = $builder->getProposals();
        foreach ($proposals as $proposal => $value) {
            $outputFile = $this->outputFile($proposal);
            if (is_dir($outputFile) === true) {
                throw new IOException("Cannot create {$outputFile} file -- A directory with same name is exist!");
            }

            if (file_put_contents($outputFile, json_encode($value)) === false) {
                throw new IOException("Cannot create {$outputFile} file -- Permission denied!");
            }
        }
        return true;
    }

    /**
     * Determines absolute path to store proposal file to.
     *
     * @param string $fileName
     * @return string File to store proposal to
     * @access public
     */
    public function outputFile($fileName) {
        return $this->outputDir() . DIRECTORY_SEPARATOR . $fileName . '.json';
    }

    /**
     * Determines absolute path to store proposal files to.
     *
     * @return string Directory where proposal files are stored
     * @access public
     */
    public function outputDir() {
        return $this->config['outputRoot'] . DIRECTORY_SEPARATOR . $this->config['name'] . '.bundle';
    }

}
