<!--
/*
 *
 * This script is part of NethServer.
 *
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see COPYING.
 */
-->

<template>
  <div>
    <h2>{{ $t('NfsSharedfolders.title') }}</h2>
    <div v-if="!view.isLoaded" class="spinner spinner-lg view-spinner"></div>
    <div v-show="view.isLoaded">
      <!-- <h3 v-if="sharedfolders.length > 0">{{$t('NfsSharedfolders.actions')}}</h3>
      <div v-if="sharedfolders.length > 0" class="btn-group">
        <button
          @click="openCreateDyndns()"
          class="btn btn-primary btn-lg"
        >{{$t('NfsSharedfolders.create_sharedfolders')}}</button>
      </div> -->
      <h3 v-if="sharedfolders.length > 0">{{$t('NfsSharedfolders.sharedfolders_list')}}</h3>
      <div v-if="sharedfolders.length > 0" class="row">
        <form role="form" class="search-pf has-button search col-sm-6 no-padding-left">
          <div class="form-group has-clear">
            <div class="search-pf-input-group">
              <label class="sr-only">Search</label>
              <input
                v-focus
                type="search"
                v-model="searchString"
                class="form-control input-lg"
                :placeholder="$t('NfsSharedfolders.search')+'...'"
              >
            </div>
          </div>
        </form>
      </div>
      <div v-if="sharedfolders.length == 0" class="blank-slate-pf">
        <div class="blank-slate-pf-icon">
          <span class="pf-icon pf-icon-process-automation"></span>
        </div>
        <h1>{{$t('NfsSharedfolders.jobs_not_found')}}</h1>
        <p>{{$t('NfsSharedfolders.jobs_not_found_desc')}}.</p>
      </div>
      <div
        v-if="sharedfolders.length > 0"
        class="list-group list-view-pf list-view-pf-view no-mg-top mg-top-10"
      >
        <div
          v-for="(m, mk) in filteredSharedfolders"
          v-bind:key="mk"
          :class="['list-group-item', m.NfsStatus == 'disabled' ? 'gray' : '']"
        >
          <div  class="list-view-pf-actions">
            <button
              @click="m.NfsStatus == 'disabled' ? toggleStatusSharedfolders(m) : openEditSharedfolders(m)"
              :class="['btn btn-default', m.NfsStatus == 'disabled' ? 'btn-primary' : '']"
            >
              <span
                :class="['fa', m.NfsStatus == 'disabled' ? 'fa-check' : 'fa-pencil', 'span-right-margin']"
              ></span>
              {{m.NfsStatus == 'disabled' ? $t('enable') : $t('edit')}}
            </button>
            <div class="dropup pull-right dropdown-kebab-pf">
              <button
                class="btn btn-link dropdown-toggle"
                type="button"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="true"
              >
                <span class="fa fa-ellipsis-v"></span>
              </button>
              <ul class="dropdown-menu dropdown-menu-right">
                <li>
                  <a @click="toggleStatusSharedfolders(m)">
                    <span
                      :class="['fa', m.NfsStatus == 'enabled' ? 'fa-lock' : 'fa-check', 'span-right-margin']"
                    ></span>
                    {{m.NfsStatus == 'enabled' ? $t('disable') : $t('enable')}}
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div  class="list-view-pf-main-info small-list">
            <div class="list-view-pf-left">
              <span :class="['fa', 'list-view-pf-icon-sm', 'pf pficon-folder-open']"></span>
            </div>
            <div class="list-view-pf-body">
              <div class="list-view-pf-description">
                <div class="list-group-item-heading">{{m.name}}</div>
                <div class="list-group-item-text">{{m.Description}}</div>
              </div>
              <div class="list-view-pf-additional-info rules-info"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="modal" id="editNfsSharedfolderModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4
              class="modal-title"
              >{{$t('NfsSharedfolders.edit_sharedfolder') + ' '+ currentSharedfolder.name }}
            </h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="saveDyndns(currentSharedfolder)">
            <div class="modal-body">
              <div 
                :class="['form-group', currentSharedfolder.errors.name.hasError ? 'has-error' : '']"
              >
                <label
                  :class="['col-sm-5', 'control-label']"
                  for="textInput-modal-markup"
                >{{$t('NfsSharedfolders.name')}}</label>
                <div :class="'col-sm-7'">
                  <input  
                    disabled type="text" v-model="currentSharedfolder.name" class="form-control"
                  >
                  <span
                    v-if="currentSharedfolder.errors.name.hasError"
                    class="help-block"
                  >
                    {{$t('validation.validation_failed')}}: 
                    {{$t('validation.'+currentSharedfolder.errors.name.message)}}
                  </span>
                </div>
              </div>
              
              <div :class="['form-group', currentSharedfolder.errors.Description.hasError ? 'has-error' : '']">
                <label
                  :class="['col-sm-5', 'control-label']"
                  for="textInput-modal-markup"
                >
                  {{$t('NfsSharedfolders.Description')}}
                </label>
                <div :class="'col-sm-7'">
                  <input disabled type="text" v-model="currentSharedfolder.Description" class="form-control">
                  <span
                    v-if="currentSharedfolder.errors.Description.hasError"
                    class="help-block"
                  >
                    {{$t('validation.validation_failed')}} : 
                    {{$t('validation.'+currentSharedfolder.errors.Description.message)}}
                  </span>
                </div>
              </div>
              <div  
                :class="['form-group', currentSharedfolder.errors.NfsLocalNetwork.hasError ? 'has-error' : '']"
               >
                <label
                    :class="['col-sm-5', 'control-label']"
                    for="textInput-modal-markup"
                >
                  {{$t('NfsSharedfolders.NfsLocalNetwork')}}
                </label>
                <div :class="'col-sm-7'">
                <input  
                    id='NfsLocalNetwork' type="checkbox" true-value="enabled" 
                    false-value="disabled" v-model="currentSharedfolder.NfsLocalNetwork" 
                >
                  <span
                    v-if="currentSharedfolder.errors.NfsLocalNetwork.hasError"
                    class="help-block"
                  >
                  {{$t('validation.validation_failed')}} : 
                  {{$t('validation.'+currentSharedfolder.errors.NfsLocalNetwork.message)}}
                </span>
                </div>
              </div>
              <div 
                :class="['form-group', currentSharedfolder.errors.AllowedIP.hasError ? 'has-error' : '']">
                <label
                  class="col-sm-5 control-label"
                  for="textInput-modal-markup"
                >
                  {{$t('NfsSharedfolders.AllowedIP')}}
                </label>
                <div class="col-sm-7">
                  <textarea v-model="currentSharedfolder.AllowedIP" class="form-control"></textarea>
                  <span v-if="currentSharedfolder.errors.AllowedIP.hasError" class="help-block">
                    {{$t('validation.validation_failed')}}:
                    {{$t('validation.'+currentSharedfolder.errors.AllowedIP.message)}}: 
                        {{currentSharedfolder.errors.AllowedIP.value}}
                  </span>
                </div>
              </div>
              <div  
                :class="['form-group', currentSharedfolder.errors.GroupAccess.hasError ? 'has-error' : '']"
               >
                <label
                    :class="['col-sm-5', 'control-label']"
                    for="textInput-modal-markup"
                >
                  {{$t('NfsSharedfolders.AllowWriting')}}
                </label>
                <div :class="'col-sm-7'">
                <input  
                    id='GroupAccess' type="checkbox" true-value="rw" 
                    false-value="r" v-model="currentSharedfolder.GroupAccess" 
                >
                  <span
                    v-if="currentSharedfolder.errors.GroupAccess.hasError"
                    class="help-block"
                  >
                  {{$t('validation.validation_failed')}} : 
                  {{$t('validation.'+currentSharedfolder.errors.GroupAccess.message)}}
                </span>
                </div>
              </div>
              <div v-if="accountsProvider==='ad'">
                <div  
                  :class="['form-group', currentSharedfolder.errors.NfsUserID.hasError ? 'has-error' : '']"
                 >
                  <label
                      :class="['col-sm-5', 'control-label']"
                      for="textInput-modal-markup"
                  >
                    {{$t('NfsSharedfolders.NfsUserID')}}
                  </label>
                  <div :class="'col-sm-7'">
                  <input  
                      id='NfsUserID' type="checkbox" true-value="enabled" 
                      false-value="disabled" v-model="currentSharedfolder.NfsUserID" 
                  >
                    <span
                      v-if="currentSharedfolder.errors.NfsUserID.hasError"
                      class="help-block"
                    >
                    {{$t('validation.validation_failed')}} : 
                    {{$t('validation.'+currentSharedfolder.errors.NfsUserID.message)}}
                  </span>
                  </div>
                </div>
                <div  v-if= "currentSharedfolder.NfsUserID === 'enabled'"
                  :class="['form-group', currentSharedfolder.errors.NfsRootSquash.hasError ? 'has-error' : '']"
                 >
                  <label
                      :class="['col-sm-5', 'control-label']"
                      for="textInput-modal-markup"
                  >
                    {{$t('NfsSharedfolders.NfsRootSquash')}}
                  </label>
                  <div :class="'col-sm-7'">
                  <input  
                    id='NfsRootSquash' type="checkbox" true-value="root_squash" 
                    false-value="no_root_squash" v-model="currentSharedfolder.NfsRootSquash" 
                  >
                    <span
                      v-if="currentSharedfolder.errors.NfsRootSquash.hasError"
                      class="help-block"
                    >
                    {{$t('validation.validation_failed')}} : 
                    {{$t('validation.'+currentSharedfolder.errors.NfsRootSquash.message)}}
                  </span>
                  </div>
                </div>
                <div v-if= "currentSharedfolder.NfsUserID === 'enabled'"
                  :class="['form-group', currentSharedfolder.errors.NfsViewGid.hasError ? 'has-error' : '']"
                >
                  <label
                    :class="['col-sm-5', 'control-label']"
                    for="textInput-modal-markup"
                  >{{$t('NfsSharedfolders.NfsViewGid')}}</label>
                  <div :class="'col-sm-7'">
                    <input  
                      disabled type="text" v-model="currentSharedfolder.NfsViewGid" class="form-control"
                    >
                    <span
                      v-if="currentSharedfolder.errors.NfsViewGid.hasError"
                      class="help-block"
                    >
                      {{$t('validation.validation_failed')}}: 
                      {{$t('validation.'+currentSharedfolder.errors.NfsViewGid.message)}}
                    </span>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <legend class=" col-sm-5 control-label fields-section-header-pf" aria-expanded="true">
                  <span
                    :class="['fa fa-angle-right field-section-toggle-pf', currentSharedfolder.advanced ? 'fa-angle-down' : '']"
                  ></span>
                  <a
                    class="field-section-toggle-pf"
                    @click="toggleAdvancedMode()"
                  >{{$t('NfsSharedfolders.advanced_mode')}}</a>
                </legend>
              </div>
              <div  v-if= "currentSharedfolder.advanced"
                :class="['form-group', currentSharedfolder.errors.NfsSync.hasError ? 'has-error' : '']"
               >
                <label
                    :class="['col-sm-5', 'control-label']"
                    for="textInput-modal-markup"
                >
                  {{$t('NfsSharedfolders.NfsSync')}}
                </label>
                <div :class="'col-sm-7'">
                <input  
                  id='NfsSync' type="checkbox" true-value="sync" 
                  false-value="async" v-model="currentSharedfolder.NfsSync" 
                >
                  <span
                    v-if="currentSharedfolder.errors.NfsSync.hasError"
                    class="help-block"
                  >
                  {{$t('validation.validation_failed')}} : 
                  {{$t('validation.'+currentSharedfolder.errors.NfsSync.message)}}
                </span>
                </div>
              </div>
              <div  v-if= "currentSharedfolder.advanced"
                :class="['form-group', currentSharedfolder.errors.NfsWdelay.hasError ? 'has-error' : '']"
               >
                <label
                    :class="['col-sm-5', 'control-label']"
                    for="textInput-modal-markup"
                >
                  {{$t('NfsSharedfolders.NfsWdelay')}}
                </label>
                <div :class="'col-sm-7'">
                <input  
                  id='NfsWdelay' type="checkbox" true-value="wdelay" 
                  false-value="no_wdelay" v-model="currentSharedfolder.NfsWdelay" 
                >
                  <span
                    v-if="currentSharedfolder.errors.NfsWdelay.hasError"
                    class="help-block"
                  >
                  {{$t('validation.validation_failed')}} : 
                  {{$t('validation.'+currentSharedfolder.errors.NfsWdelay.message)}}
                </span>
                </div>
              </div>
              <div  v-if= "currentSharedfolder.advanced"
                :class="['form-group', currentSharedfolder.errors.NfsSecure.hasError ? 'has-error' : '']"
               >
                <label
                    :class="['col-sm-5', 'control-label']"
                    for="textInput-modal-markup"
                >
                  {{$t('NfsSharedfolders.NfsSecure')}}
                </label>
                <div :class="'col-sm-7'">
                <input  
                  id='NfsSecure' type="checkbox" true-value="secure" 
                  false-value="insecure" v-model="currentSharedfolder.NfsSecure" 
                >
                  <span
                    v-if="currentSharedfolder.errors.NfsSecure.hasError"
                    class="help-block"
                  >
                  {{$t('validation.validation_failed')}} : 
                  {{$t('validation.'+currentSharedfolder.errors.NfsSecure.message)}}
                </span>
                </div>
              </div>
              <div  v-if= "currentSharedfolder.advanced"
                :class="['form-group', currentSharedfolder.errors.NfsHide.hasError ? 'has-error' : '']"
               >
                <label
                    :class="['col-sm-5', 'control-label']"
                    for="textInput-modal-markup"
                >
                  {{$t('NfsSharedfolders.NfsHide')}}
                </label>
                <div :class="'col-sm-7'">
                <input  
                  id='NfsHide' type="checkbox" true-value="nohide" 
                  false-value="hide" v-model="currentSharedfolder.NfsHide" 
                >
                  <span
                    v-if="currentSharedfolder.errors.NfsHide.hasError"
                    class="help-block"
                  >
                  {{$t('validation.validation_failed')}} : 
                  {{$t('validation.'+currentSharedfolder.errors.NfsHide.message)}}
                </span>
                </div>
              </div>
              <div class="modal-footer">
                <div v-if="currentSharedfolder.isLoading" class="spinner spinner-sm form-spinner-loader"></div>
                <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
                <button
                  class="btn btn-primary"
                  type="submit"
                >{{currentSharedfolder.isEdit ? $t('edit') : $t('save')}}</button>
              </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NfsSharedfolders",
  mounted() {
    this.getSharedFolders();
  },
  beforeRouteLeave(to, from, next) {
    $(".modal").modal("hide");
    next();
  },
  data() {
    return {
      view: {
        isLoaded: false,
      },
      searchString: "",
      sharedfolders: [],
      currentSharedfolder: this.initSharedfolders(),
      advanced: false,
      accountsProvider: "none"
    };
  },
  computed: {
    filteredSharedfolders() {
      var returnObj = [];
      for (var r in this.sharedfolders) {
        var cat = JSON.stringify(this.sharedfolders[r]);
        if (cat.toLowerCase().includes(this.searchString.toLowerCase())) {
          returnObj.push(this.sharedfolders[r]);
        }
      }

      return returnObj;
    }
  },
  methods: {
    initSharedfolders() {
      return {
        name: "",
        Description: "",
        NfsLocalNetwork:"",
        AllowedIP:"",
        GroupAccess:"",
        NfsUserID:"",
        NfsRootSquash: "",
        NfsViewGid: "",
        NfsSync:"",
        NfsWdelay:"",
        NfsSecure:"",
        NfsHide:"",
        NfsStatus:"disabled",
        errors: this.initSharedfoldersErrors(),
        isLoading: false,
      };
    },
    initSharedfoldersErrors() {
      return {
        name: {
          hasError: false,
          message: ""
        },
        NfsLocalNetwork: {
          hasError: false,
          message: ""
        },
        Description: {
          hasError: false,
          message: ""
        },
        AllowedIP: {
          hasError: false,
          message: ""
        },
        GroupAccess: {
          hasError: false,
          message: ""
        },
        NfsUserID: {
          hasError: false,
          message: ""
        },
        NfsRootSquash: {
          hasError: false,
          message: ""
        },
        NfsViewGid: {
          hasError: false,
          message: ""
        },
        NfsSync: {
          hasError: false,
          message: ""
        },
        NfsWdelay: {
          hasError: false,
          message: ""
        },
        NfsSecure: {
          hasError: false,
          message: ""
        },
        NfsHide: {
          hasError: false,
          message: ""
        }
      };
    },
    toggleAdvancedMode() {
      this.currentSharedfolder.advanced = !this.currentSharedfolder.advanced;
      this.$forceUpdate();
    },
    getSharedFolders() {
      var context = this;
      context.view.isLoaded = false;
      nethserver.exec(
        ["nethserver-nfs/read"],
        {
          action: "list"
        },
        null,
        function(success) {
          try {
            success = JSON.parse(success);
          } catch (e) {
            console.error(e);
          }
          context.sharedfolders = success.sharedfolders;
          context.accountsProvider = success.accountsProvider;
          context.view.isLoaded = true;
        },
        function(error) {
          console.error(error);
            context.view.isLoaded = true;
        }
      );
    },
    openEditSharedfolders(job) {
      this.currentSharedfolder = JSON.parse(JSON.stringify(job));
      this.currentSharedfolder.errors = this.initSharedfoldersErrors();
      this.currentSharedfolder.AllowedIP = this.currentSharedfolder.AllowedIP.split(",").join("\n");
      // this.currentSharedfolder.isEdit = true;
      this.currentSharedfolder.isLoading = false;
      this.currentSharedfolder.advanced = false;
      // this.togglePass = true;
      $("#editNfsSharedfolderModal").modal("show");
    },
    saveDyndns(sharedfolder) {
      var context = this;

      var sharedfoldersObj = {
        action: "update",
        name: sharedfolder.name,
        NfsLocalNetwork: sharedfolder.NfsLocalNetwork,
        AllowedIP:  sharedfolder.AllowedIP.split("\n").join(","),
        GroupAccess:sharedfolder.GroupAccess,
        NfsRootSquash: sharedfolder.NfsRootSquash,
        NfsUserID: sharedfolder.NfsUserID,
        NfsSync: sharedfolder.NfsSync,
        NfsWdelay:sharedfolder.NfsWdelay,
        NfsSecure:sharedfolder.NfsSecure,
        NfsHide:sharedfolder.NfsHide
      };

      context.currentSharedfolder.isLoading = true;
      context.$forceUpdate();
      nethserver.exec(
        ["nethserver-nfs/validate"],
        sharedfoldersObj,
        null,
        function(success) {
          context.currentSharedfolder.isLoading = false;
          $("#editNfsSharedfolderModal").modal("hide");

          // notification
          nethserver.notifications.success = context.$i18n.t(
            "NfsSharedfolders.sharedfolders_updated_ok");

          nethserver.notifications.error = context.$i18n.t(
            "NfsSharedfolders.sharedfolders_updated_error");

          nethserver.exec(
              ["nethserver-nfs/update"],
              sharedfoldersObj,
              function(stream) {
                console.info("job-edit", stream);
              },
              function(success) {
                // get all
                context.getSharedFolders();
              },
              function(error, data) {
                console.error(error, data);
              }
            );
        },
        function(error, data) {
          var errorData = {};
          context.currentSharedfolder.isLoading = false;
          context.currentSharedfolder.errors = context.initSharedfoldersErrors();

          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.currentSharedfolder.errors[attr.parameter].hasError = true;
              context.currentSharedfolder.errors[attr.parameter].message = attr.error;
              context.currentSharedfolder.errors[attr.parameter].value = attr.value;
              context.$forceUpdate();
            }
          } catch (e) {
            console.error(e);
          }
        }
      );
    },
    toggleStatusSharedfolders(job) {
      var context = this;
      // notification
      nethserver.notifications.success = context.$i18n.t(
        "NfsSharedfolders.sharedfolders_updated_ok"
      );
      nethserver.notifications.error = context.$i18n.t(
        "NfsSharedfolders.sharedfolders_updated_error"
      );

      // update values
      nethserver.exec(
        ["nethserver-nfs/update"],
        {
          action: job.NfsStatus == "enabled" ? "disable" : "enable",
          name: job.name
        },
        function(stream) {
          console.info("update-status", stream);
        },
        function(success) {
          // get all
          context.getSharedFolders();
        },
        function(error, data) {
          console.error(error, data);
        }
      );
    }
  }
};
</script>

<style>
.list-group-item-heading {
  width: calc(50% - 20px) !important;
}
.list-group-item-text {
  width: calc(50% - 40px) !important;
}
.list-view-pf-description {
  flex: 1 0 70% !important;
}
.list-view-pf-actions {
  z-index: 2;
}
.remove-cat {
  margin-top: 6px;
  color: dimgrey;
}
.remove-cat:hover {
  cursor: pointer;
  color: #39a5dc;
}

.adjust-mg-bottom {
  margin-bottom: 4px;
}
.adjust-divider {
  margin-top: 15px;
}
.adjust-filter-cat {
  margin-top: 5px;
}

.right {
  float: right;
}

.eachCheckBox {
  margin-left: 20px;
}

.green {
  color: #3f9c35;
}
.red {
  color: #cc0000;
}
.gray {
  color: gray;
}

.no-padding-left {
  padding-left: 0px;
}
</style>
