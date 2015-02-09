<?php
/**
 * @copyright	Copyright (C) 2005 - 2012 Open Source Matters, Inc. All rights reserved.
 * @license		GNU General Public License version 2 or later; see LICENSE.txt
 */

// no direct access
defined('_JEXEC') or die;

/**
 * Utility class working with system
 *
 * @package		Joomla.Administrator
 * @subpackage	com_admin
 * @since		1.6
 */
abstract class JHtmlSystem
{
	/**
	 * method to generate a string message for a value
	 *
	 * @param string $val a php ini value
	 *
	 * @return string html code
	 */
	public static function server($val)
	{
		if (empty($val)) {
			return JText::_('COM_ADMIN_NA');
		}
		else {
			return $val;
		}
	}
}
