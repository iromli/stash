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

use \ReflectionClass;

/**
 * ClassInspector
 *
 * @package reflextor
 * @subpackage reflextor.inspector
 * @author Isman Firmansyah
 */
class ClassInspector extends \reflextor\inspector\BaseInspector {

    /**
     * Sets instance of <tt>ReflectionClass</tt> as reflector object.
     *
     * @return void
     * @access public
     */
    public function __construct(ReflectionClass $reflector) {
        parent::__construct($reflector);
    }

    /**
     * Gets constructor parameters if class is constructable.
     *
     * @return string|array A list of constructor parameters or empty string
     * @access public
     */
    public function getParameters() {
        $params = '';
        $constructor = $this->reflector->getConstructor();
        if ($constructor !== null) {
            $constructor_params = $constructor->getParameters();
            foreach ($constructor_params as $param) {
                $type = ($param->isOptional() === true) ? 'optional' : 'required';
                $params[$type][] = $param->getName();
            }
        }
        return $params;
    }

}
