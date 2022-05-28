<?php
/**
 * Reflextor - Reflection extractor
 *
 * @author      Isman Firmansyah
 * @copyright   2011 Isman Firmansyah
 * @link        https://github.com/iromli/reflextor
 * @license     http://opensource.org/licenses/mit-license.php The MIT License
 */

namespace reflextor\util;

/**
 * DocBlockParser
 *
 * @package reflextor
 * @subpackage reflextor.util
 * @author Isman Firmansyah
 */
class DocBlockParser {

    /**
     * Strips asterisks and slashes from docblock comment.
     *
     * @param string $comments Docblock comment
     * @return string Stripped docblock comment
     * @access public
     */
    public static function parse($comments) {
        //remove stars and slashes
        $comments = preg_replace('#^(\s*/\*\*|\s*\*+/|\s+\* ?)#m', '', $comments);

        //fix new lines
        $comments = str_replace("\r\n", "\n", $comments);
        return ltrim($comments, "\n");
    }

}
