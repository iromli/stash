<?php
/**
 * Reflextor - Reflection extractor
 *
 * @author      Isman Firmansyah
 * @copyright   2011 Isman Firmansyah
 * @link        https://github.com/iromli/reflextor
 * @license     http://opensource.org/licenses/mit-license.php The MIT License
 */

namespace reflextor\inspector;

use \reflector\util\DocBlockParser;

/**
 * BaseInspector
 *
 * @package reflextor
 * @subpackage reflextor.inspector
 * @author Isman Firmansyah
 */
class BaseInspector {

    /**
     * Sets reflector object.
     *
     * @return void
     * @access public
     */
    public function __construct($reflector) {
        $this->reflector = $reflector;
    }

    /**
     * Gets reflector name.
     *
     * @return string Reflector name
     * @access public
     */
    public function getName() {
        return $this->reflector->getName();
    }

    /**
     * Gets reflector docblock comment.
     *
     * If reflector docblock comment isn't false, the returned comment is stripped.
     *
     * @return string Stripped docblock comment or empty string
     * @access public
     */
    public function getInfo() {
        $info = $this->reflector->getDocComment();
        return ($info === false) ? '' : DocBlockParser::parse($info);
    }

    /**
     * Gets function or method parameters.
     *
     * @return string|array A list of function or method parameters or empty string
     * @access public
     */
    public function getParameters() {
        return '';
    }

    /**
     * Gets proposal for code completion.
     *
     * @return array A proposal consists of name, info, and parameters
     * @access public
     */
    public function getProposal() {
        $name   = $this->getName();
        $info   = $this->getInfo();
        $params = $this->getParameters();
        return compact('name', 'info', 'params');
    }

}
