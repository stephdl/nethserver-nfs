<?php
/* @var $view \Nethgui\Renderer\Xhtml */

echo $view->fieldsetSwitch('NfsStatus', 'enabled', $view::FIELDSETSWITCH_CHECKBOX)->setAttribute('uncheckedValue', 'disabled')
    // ->setAttribute('icon-before', 'ui-icon-link')

->insert($view->checkbox('NfsLocalNetwork', 'enabled')->setAttribute('uncheckedValue', 'disabled'))
->insert($view->textArea('AllowedIP', $view::LABEL_ABOVE)->setAttribute('dimensions', '5x30'))
    ->insert($view->checkBox('AllowWriting', 'rw')->setAttribute('uncheckedValue', 'r'));


if ($view['isAD']) {
    $gid = $view->fieldsetSwitch('NfsUserID', 'enabled', $view::FIELDSETSWITCH_CHECKBOX | $view::FIELDSETSWITCH_EXPANDABLE)->setAttribute('uncheckedValue', 'disabled');
    $gid ->insert($view->checkbox('NfsRootSquash', 'root_squash')->setAttribute('uncheckedValue', 'no_root_squash'));
    $gid ->insert($view->textinput('viewgid',$view::STATE_DISABLED|$view::LABEL_ABOVE));
    echo ($gid);
}

echo $view->fieldset('', $view::FIELDSET_EXPANDABLE)->setAttribute('template', $T('NfsAdvanced_label'))
->insert($view->checkbox('NfsSync', 'sync')->setAttribute('uncheckedValue', 'async'))
->insert($view->checkbox('NfsWdelay', 'wdelay')->setAttribute('uncheckedValue', 'no_wdelay'))
->insert($view->checkbox('NfsSecure', 'secure')->setAttribute('uncheckedValue', 'insecure'))
->insert($view->checkbox('NfsHide', 'nohide')->setAttribute('uncheckedValue', 'hide'))
;
