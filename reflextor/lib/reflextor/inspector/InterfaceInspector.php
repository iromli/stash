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
 * InterfaceInspector
 *
 * @package reflextor
 * @subpackage reflextor.inspector
 * @author Isman Firmansyah
 */
class InterfaceInspector extends \reflextor\inspector\BaseInspector {

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
     * Gets proposal for code completion.
     *
     * @return array A proposal consists of name, info, and parameters
     * @access public
     */
    public function getProposal() {
        $name = $this->getName();
        $info = $this->getInfo();
        $type = 'interface';
        return compact('name', 'info', 'type');
    }

}
