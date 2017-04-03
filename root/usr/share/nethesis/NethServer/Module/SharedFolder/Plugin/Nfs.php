<?php
namespace NethServer\Module\SharedFolder\Plugin;

use Nethgui\System\PlatformInterface as Validate;
use Nethgui\Controller\Table\Modify as Table;

/**
 * Nfs SharedFolder plugin
 *
 * @author stephane de labrusse <stephdl@de-labrusse.fr>
 *
 */
class  Nfs  extends \Nethgui\Controller\Table\RowPluginAction
{

    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $base)
    {
        return \Nethgui\Module\SimpleModuleAttributesProvider::extendModuleAttributes($base, 'Nfs', 20);
    }


    public function initialize()
    {

        $schema = array(
            array('NfsStatus', Validate::SERVICESTATUS, Table::FIELD, 'NfsStatus'),
            array('NfsLocalNetwork', Validate::SERVICESTATUS, Table::FIELD, 'NfsLocalNetwork'),
            array('AllowedIP', $this->createValidator(TRUE), Table::FIELD, 'AllowedIP'),
            array('AllowWriting', $this->createValidator()->memberOf('r','rw'), Table::FIELD, 'GroupAccess'),
            array('NfsSync', $this->createValidator()->memberOf('sync','async'), Table::FIELD, 'NfsSync'),
            array('NfsWdelay', $this->createValidator()->memberOf('wdelay','no_wdelay'), Table::FIELD, 'NfsWdelay'),
            array('NfsSecure', $this->createValidator()->memberOf('secure','insecure'), Table::FIELD, 'NfsSecure'),
            array('NfsHide', $this->createValidator()->memberOf('nohide','hide'), Table::FIELD, 'NfsHide'),
            array('NfsUserID', Validate::SERVICESTATUS, Table::FIELD, 'NfsUserID'),
            array('NfsRootSquash', $this->createValidator()->memberOf('root_squash','no_root_squash'), Table::FIELD, 'NfsRootSquash'),
            array('ibay', Validate::ANYTHING, Table::KEY),
        );

        $this
            ->declareParameter('NfsStatus')->setDefaultValue('NfsStatus', 'enabled')
            ->declareParameter('NfsLocalNetwork')->setDefaultValue('NfsLocalNetwork', 'disabled')
            ->declareParameter('NfsRW')->setDefaultValue('NfsRW', 'ro')
            ->declareParameter('NfsSync')->setDefaultValue('NfsSync', 'sync')
            ->declareParameter('NfsWdelay')->setDefaultValue('NfsWdelay', 'wdelay')
            ->declareParameter('NfsSquash')->setDefaultValue('NfsSquash', 'all_squash')
            ->declareParameter('NfsSecure')->setDefaultValue('NfsSecure', 'secure')
            ->declareParameter('NfsHide')->setDefaultValue('NfsHide', 'nohide')
            ->declareParameter('NfsUserID')->setDefaultValue('NfsUserID', 'enabled')
            ->declareParameter('NfsRootSquash')->setDefaultValue('NfsRootSquash', 'root_squash')
            ->declareParameter('ibay')
        ;

        $this->setSchemaAddition($schema);
        parent::initialize();
    }


    public static function splitLines($text)
    {
        return array_filter(preg_split("/[,;\s]+/", $text));
    }

    public function readAllowedIP($dbList)
    {
        return implode("\r\n", explode(',' ,$dbList));
    }

    public function writeAllowedIP($viewText)
    {
        return array(implode(',', self::splitLines($viewText)));
    }

    private function readgid()
    {
        $ibay = $this->parameters['ibay'];
        $gid = $this->getPlatform()->exec('/usr/libexec/nethserver/getentGroupNfs '. $ibay)->getOutput();
        return ($gid);
    }

    public function bind(\Nethgui\Controller\RequestInterface $request)
    {
        parent::bind($request);
        $this->gid = $this->readgid();
    }



    public function validate(\Nethgui\Controller\ValidationReportInterface $report)
    {
        parent::validate($report);
        $itemValidator = $this->getPlatform()->createValidator(\Nethgui\System\PlatformInterface::IP);

        foreach (self::splitLines($this->parameters['AllowedIP']) as $v) {
            if ( ! $itemValidator->evaluate($v)) {
                $report->addValidationErrorMessage($this, 'AllowedIP', 'IP address list', array($v));
                break;
            }
        }
    }

   public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        parent::prepareView($view);

        if (!$this->gid) {
            $this->gid = $this->readgid();
        }
        $view['viewgid'] = $this->gid;

    }

}
