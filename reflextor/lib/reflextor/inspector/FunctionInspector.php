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

use \ReflectionFunction;

/**
 * FunctionInspector
 *
 * @package reflextor
 * @subpackage reflextor.inspector
 * @author Isman Firmansyah
 */
class FunctionInspector extends \reflextor\inspector\BaseInspector {

    /**
     * Sets instance of <tt>ReflectionFunction</tt> as reflector object.
     *
     * @return void
     * @access public
     */
    public function __construct(ReflectionFunction $reflector) {
        parent::__construct($reflector);
    }

    /**
     * Gets function parameters.
     *
     * @return string|array A list of function parameters or empty string
     * @access public
     */
    public function getParameters() {
        $params = '';
        $functionParams = $this->reflector->getParameters();
        foreach ($functionParams as $param) {
            $type = ($param->isOptional() === true) ? 'optional' : 'required';
            $params[$type][] = $param->getName();
        }
        return $params;
    }

}
