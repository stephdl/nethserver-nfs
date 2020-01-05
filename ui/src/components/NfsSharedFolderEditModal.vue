<!--
#
# Copyright (C) 2019 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#
-->

<style scoped>
.pd-indent {
    margin-left: 8px;
}
textarea {
    width: 100%;
    min-height: 7em;
    font-family: monospace;
}
select {
    padding: 0;
}

.alert-title {
    display: inline-block;
    margin-right: 1ex;
}

.inline-select {
  display: inline-block !important;
  margin: 5px;
}

.label-select {
  padding: 8px;
}

.label-acl {
  color: #363636;
  background: #f5f5f5;
}

.remove-acl {
  color: #363636;
}

.builtin-acl {
  color: #909090;
  cursor: not-allowed;
}
</style>

<template>
    <div v-bind:id="id" data-backdrop="static" class="modal" tabindex="-1" role="dialog" v-bind:aria-labelledby="id + 'Label'" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true" aria-label="Close">
                        <span class="pficon pficon-close"></span>
                    </button>
                    <h4 class="modal-title" v-bind:id="id + 'Label'">
                        <!-- <span v-if="action == 'delete'"      >{{ $t('NfsSharedfolders.delete_title', this.item) }}</span>
                        <span v-else-if="action == 'reset-permissions'" >{{ $t('NfsSharedfolders.reset_permissions_title', this.item) }}</span>
                        <span v-else-if="action == 'migrate'" >{{ $t('NfsSharedfolders.migrate_title', this.item) }}</span>
                        <span v-else-if="action == 'create'" >{{ $t('NfsSharedfolders.create_title', this.item) }}</span> -->
                        <span >{{ $t('NfsSharedfolders.edit_title',   this.item) }}</span>
                    </h4>
                </div>

                <!-- <div v-if="action == 'delete'" class="modal-body">
                    <div class="alert alert-warning">
                        <span class="pficon pficon-warning-triangle-o"></span>
                        <strong class="alert-title">{{$t('NfsSharedfolders.delete_warning_title', this.item)}}</strong>&#x20;
                        <i18n path="sharedfolders.delete_warning_message" tag="span">
                            <b place="name">{{ this.item.name }}</b>
                        </i18n>
                    </div>
                    <div>{{ $t('NfsSharedfolders.delete_confirm_message', this.item) }}</div>
                </div> -->

                <!-- <div v-else-if="action == 'reset-permissions'" class="modal-body">
                    <div class="alert alert-warning">
                        <span class="pficon pficon-warning-triangle-o"></span>
                        <strong class="alert-title">{{$t('NfsSharedfolders.reset_permissions_warning_title', this.item)}}</strong>&#x20;
                        <span>{{ $t('NfsSharedfolders.reset_permissions_warning_message')}}</span>
                    </div>
                    <div>
                        <i18n path="sharedfolders.reset_permissions_confirm_message" tag="span">
                            <b place="name">{{ this.item.name }}</b>
                        </i18n>
                    </div>
                </div> -->

                <!-- <div v-else-if="action == 'migrate'" class="modal-body">
                    <div class="alert alert-warning">
                        <span class="pficon pficon-warning-triangle-o"></span>
                        <strong class="alert-title">{{$t('NfsSharedfolders.migrate_warning_title', this.item)}}</strong>&#x20;
                        <span>{{ $t('NfsSharedfolders.migrate_warning_message') }}</span>
                    </div>
                    <div>
                        <i18n path="sharedfolders.migrate_confirm_message" tag="span">
                            <b place="vhost">{{
                                item.migrateVhost == '__ANY__' ? $t('NfsSharedfolders.vhost_default') : item.migrateVhost
                            }}</b>
                        </i18n>
                    </div>
                </div> -->

                <div class="modal-body">
                    <div v-if="!vIsAd" class="alert alert-info">
                        <span class="pficon pficon-info"></span>
                        <strong class="alert-title">{{$t('NfsSharedfolders.no_acls_support_title', this.item)}}</strong>&#x20;
                        <span>{{ $t('NfsSharedfolders.no_acls_support_message') }}</span>
                    </div>

                    <form class="form-horizontal">
                        <div v-bind:class="['form-group', vErrors.name ? 'has-error' : '']">
                            <label class="col-sm-3 control-label" v-bind:for="id + '-ni'">{{ $t('NfsSharedfolders.name_label', this.item) }}</label>
                            <div class="col-sm-9">
                                <input v-bind:disabled="action != 'create'" type="text" v-model="item.name" v-bind:id="id + '-ni'" class="form-control">
                                <span v-if="vErrors.name" class="help-block">{{ vErrors.name }}</span>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-sm-3 control-label" v-bind:for="id + '-di'">{{ $t('NfsSharedfolders.description_label') }}</label>
                            <div class="col-sm-9">
                                <input type="text" v-model="item.Description" v-bind:id="id + '-di'" class="form-control">
                            </div>
                        </div>
              
                      <legend class="fields-section-header-pf" v-bind:aria-expanded="vAdvanced ? 'true' : 'false'">
                        <span
                            v-bind:class="['fa fa-angle-right field-section-toggle-pf', vAdvanced ? 'fa-angle-down' : '']"
                        ></span>
                        <a
                            class="field-section-toggle-pf"
                            v-on:click="() => { vAdvanced = !vAdvanced }"
                        >{{$t('advanced_mode')}}</a>
                      </legend>
                        
                      <div v-if="vAdvanced">

                      </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <span v-if="vSpinner" class="spinner spinner-xs spinner-inline form-spinner-vSpinner"></span>&#x20;
                    <button type="button" class="btn btn-default" data-dismiss="modal">{{ $t('modal_cancel_button') }}</button>
                    <!-- <button v-if="action == 'delete'" v-on:click="$emit('modal-save')" type="button" class="btn btn-danger" >{{ $t('modal_delete_button') }}</button>
                    <button v-else-if="action == 'reset-permissions'" v-on:click="$emit('modal-save')" type="button" class="btn btn-danger" >{{ $t('modal_reset_permissions_button') }}</button>
                    <button v-else-if="action == 'migrate'" v-on:click="$emit('modal-save')" type="button" class="btn btn-danger" >{{ $t('modal_migrate_button') }}</button>
                    <button v-else-if="action == 'create'" v-on:click="$emit('modal-save')" type="button" class="btn btn-primary">{{ $t('modal_create_button') }}</button> -->
                    <button v-else v-on:click="$emit('modal-save')" type="button" class="btn btn-primary">{{ $t('modal_edit_button') }}</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import execp from '@/execp'

const subjectsStore = {
    loaded: false,
    items: [],
}

export default {
    name: "NfsSharedFolderEditModal",
    props: {
        'id': String,
        'action': String,
        'initialItem': Object,
        'groupsList': Array,
        'accountsProvider': String,
    },
    watch: {
        initialItem: function(newVal) {
            Object.assign(this.item, newVal);
            this.$set(this.item, 'acls', Object.assign({EVERYONE:""}, newVal.acls))
            this.vErrors = {}
            this.vAdvanced = false
            this.vSearchText = ''
        },
    },
    computed: {
        // vOwners: function() {
        //     return [].concat(this.$props.groupsList).sort()
        // },
        // vSmbRecycleBinStatus: {
        //     get: function() {
        //         return this.item.SmbRecycleBinStatus == 'enabled'
        //     },
        //     set: function(newValue) {
        //         this.item.SmbRecycleBinStatus = newValue ? 'enabled' : 'disabled'
        //     }
        // },
        vIsAd: function() {
            return this.accountsProvider == 'ad'
        }
    },
    data() {
        return {
            vErrors: {},
            vSpinner: false,
            vAclSpinner: false,
            vAdvanced: false,
            vSearchText: '',

            item: {
                SmbRecycleBinStatus: "disabled",
                SmbRecycleBinVersionStatus: "disabled",
                SmbAuditStatus: "disabled",
                SmbShareBrowseable: "enabled",
                guestAccess: "disabled",
                name: "",
                OwningGroup: "",
                acls: {EVERYONE:""},
                Description: "",
                NfsHide:"nohide",
                NfsSecure: "secure",
                NfsLocalNetwork: "disabled",
                NfsWdelay: "wdelay",
                NfsSync: "sync",
                NfsStatus: "enabled",
                NfsUserID: "enabled",
                NfsRootSquash: "root_squash",
                NfsViewGid: ""
            }
        }
    },
    mounted: function() {
        this.$on('modal-save', (eventData) => {
            this.vSpinner = true
            var verb = 'update'
            var inputData = {
                action: this.$props['action'],
                item: Object.assign({}, this.item),
            }
            // if(this.$props['action'] == 'delete') {
            //     verb = 'delete'
            // } else if (this.$props['action'] == 'create') {
            //     verb = 'create'
            // }

            this.vErrors = {}
            execp("nethserver-nfs/sharedfolders/validate", inputData)
            .then((validationResult) => {
                this.vSpinner = false
                window.jQuery(this.$el).modal('hide') // on successful resolution close the dialog
                nethserver.notifications.success = this.$t("NfsSharedfolders.item_" + this.action + "_ok");
                nethserver.notifications.error = this.$t("NfsSharedfolders.item_" + this.action + "_error");
                return execp("nethserver-nfs/sharedfolders/" + verb, inputData, true) // start another async call
            })
            .then(() => {
                this.$emit('modal-close', eventData) // on save success, close the dialog
            })
            .catch((err) => {
                if(err.hasOwnProperty('type')) {
                    let validationError = err
                    this.vErrors = Object.fromEntries(validationError.attributes.map(err => [
                        err.parameter,
                        this.$t('validation.' + err.message.split("\n").pop(), {
                            value: err.value,
                            msg: err.message.split("\n").slice(0, -1)
                        })
                    ]))
                } else {
                    return Promise.reject(err) // throw again unhandled exceptions
                }
            })
            .finally(() => {
                this.vSpinner = false // always stop the spinner when async calls end
            })
        })
    },
    methods: {
        searchSubjects(query) {
            query = query.toLowerCase();
            if(subjectsStore.loaded) {
                return Promise.resolve(subjectsStore.items.filter(subj => subj.toLowerCase().includes(query)))
            } else {
                this.vAclSpinner = true
                return execp("nethserver-nfs/sharedfolders/read", {"action":"list-users"})
                    .then(response => {
                        this.vAclSpinner = false
                        subjectsStore.loaded = true
                        subjectsStore.items = [].concat(response.users, this.$props.groupsList).sort()
                        return subjectsStore.items.filter(subj => subj.toLowerCase().includes(query))
                    })
            }
        }
        // addSubject(subject) {
        //     if( ! this.item.acls[subject] && this.item.OwningGroup != subject) {
        //         this.$set(this.item.acls, subject, 'r') // see Vuejs "reactivity in depth"
        //     }
        // },
        // removeSubject(subject) {
        //     if(this.item.acls[subject]) {
        //         this.$delete(this.item.acls, subject)
        //     }
        // },
        // updateGownerAcl() {
        //     if( ! this.item.acls['GOWNER']) {
        //         this.$set(this.item.acls, 'GOWNER', 'rw')
        //     }
        // },
        // updateEveryoneAcl() {
        //     if( ! this.item.acls['EVERYONE']) {
        //         this.$set(this.item.acls, 'EVERYONE', 'r')
        //     }
        // },
    },
    filters: {
        shorten(subject) {
            return subject.replace(/@.*$/, '');
        },
    },
}
</script>
