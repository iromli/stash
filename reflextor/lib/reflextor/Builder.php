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

use \ReflectionFunction;
use \ReflectionClass;

use \reflextor\inspector\ClassInspector;
use \reflextor\inspector\FunctionInspector;
use \reflextor\inspector\InterfaceInspector;

/**
 * Builder
 *
 * @package reflextor
 * @author Isman Firmansyah
 */
class Builder {

    /**
     * A list of PHP internal classes.
     *
     * @var array
     * @access protected
     */
    protected $classes = array();

    /**
     * A list of PHP internal interfaces.
     *
     * @var array
     * @access protected
     */
    protected $interfaces = array();

    /**
     * A list of PHP internal functions.
     *
     * @var array
     * @access protected
     */
    protected $functions = array();

    /**
     * A list of PHP internal constants.
     *
     * @var array
     * @access protected
     */
    protected $constants = array();

    /**
     * A list of proposals.
     *
     * @var array
     * @access protected
     */
    protected $proposals = array(
        'classes'    => array(),
        'constants'  => array(),
        'interfaces' => array(),
        'functions'  => array()
    );

    private $_magicConstants = array(
        '__LINE__',
        '__FILE__',
        '__DIR__',
        '__FUNCTION__',
        '__CLASS__',
        '__METHOD__',
        '__NAMESPACE__'
    );

    /**
     * Creates a new <tt>Builder</tt>.
     *
     * @return void
     * @access public
     */
    public function __construct() {
        $this->classes = get_declared_classes();

        $this->constants = $this->_magicConstants;
        $constants = get_defined_constants(true);
        foreach ($constants as $category => $constant) {
            if ($category == 'user') {
                continue;
            }
            foreach ($constant as $name => $value) {
                $this->constants[] = $name;
            }
        }

        $this->interfaces = get_declared_interfaces();
        $this->functions  = get_defined_functions();
        $this->functions  = $this->functions['internal'];
    }

    /**
     * Gets a list of PHP internal classes.
     *
     * @return array
     * @access public
     */
    public function getClasses() {
        return $this->classes;
    }

    /**
     * Gets a list of PHP internal interfaces.
     *
     * @return array
     * @access public
     */
    public function getInterfaces() {
        return $this->interfaces;
    }

    /**
     * Gets a list of PHP internal functions.
     *
     * @return array
     * @access public
     */
    public function getFunctions() {
        return $this->functions;
    }

    /**
     * Gets a list of PHP internal constants.
     *
     * @return array
     * @access public
     */
    public function getConstants() {
        return $this->constants;
    }

    /**
     * Gets all proposals for current bundle.
     *
     * @return array
     * @access public
     */
    public function getProposals() {
        foreach ($this->classes as $class) {
            $reflector = new ReflectionClass($class);
            $inspector = new ClassInspector($reflector);
            if ($reflector->isInternal() === true) {
                $this->proposals['classes'][] = $inspector->getProposal();
            }
        }

        foreach ($this->interfaces as $interface) {
            $reflector = new ReflectionClass($interface);
            $inspector = new InterfaceInspector($reflector);
            if ($reflector->isInternal() === true) {
                $this->proposals['interfaces'][] = $inspector->getProposal();
            }
        }

        foreach ($this->functions as $function) {
            $reflector = new ReflectionFunction($function);
            $inspector = new FunctionInspector($reflector);
            $this->proposals['functions'][] = $inspector->getProposal();
        }

        foreach ($this->constants as $constant) {
            $this->proposals['constants'][] = array(
                'name'  => $constant,
                'info'  => '',
                'type'  => 'constant'
            );
        }

        return $this->proposals;
    }

}
