<!--
/*
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

<style scoped>
.spaced {
  margin-top: 1em;
}
</style>


<template>
  <div>
    <div v-if="vReadStatus == 'success' && sharedfolders.length == 0" class="blank-slate-pf">
      <div class="blank-slate-pf-icon">
        <span class="fa fa-folder-open"></span>
      </div>
      <h1>{{ $t('NfsSharedfolders.title') }}</h1>
      <p>{{ $t("sharedfolders.empty_state_message") }}</p>
      <p>
      </p>
    </div>
    <div v-else>
      <h1>{{ $t('NfsSharedfolders.title') }}</h1>
      <div v-if="vReadStatus == 'running'" class="spinner spinner-lg view-spinner"></div>
      <div v-else-if="vReadStatus == 'error'">
        <div class="alert alert-danger">
          <span class="pficon pficon-error-circle-o"></span>
          <strong>OOOPS!</strong> An unexpected error has occurred:
          <pre>{{ vReadError }}</pre>
        </div>
      </div>
      <div v-else class="spaced">
        <h3>{{$t('list_title')}}</h3>
        <nfs-shared-folders-list-view
          v-bind:items="sharedfolders"
          v-on:modal-close="read"
          v-on:item-edit="openModal('modalEditSharedFolder', $event)"
          v-on:item-delete="openModal('modalDeleteSharedFolder', $event)"
          v-on:item-reset-permissions="openModal('modalResetPermissionsSharedFolder', $event)"
          v-on:item-migrate="openModal('modalMigrateSharedFolder', $event)"
        ></nfs-shared-folders-list-view>
      </div>
    </div>

    <nfs-shared-folder-edit-modal
      id="modalCreateSharedFolder"
      action="create"
      v-on:modal-close="read($event)"
      v-bind:initial-item="currentItem"
      v-bind:groups-list="groups"
      v-bind:accounts-provider="accountsProvider"
    ></nfs-shared-folder-edit-modal>

    <nfs-shared-folder-edit-modal
      id="modalEditSharedFolder"
      action="edit"
      v-on:modal-close="read"
      v-bind:initial-item="currentItem"
      v-bind:groups-list="groups"
      v-bind:accounts-provider="accountsProvider"
    ></nfs-shared-folder-edit-modal>

    <nfs-shared-folder-edit-modal
      id="modalDeleteSharedFolder"
      action="delete"
      v-on:modal-close="read"
      v-bind:initial-item="currentItem"
    ></nfs-shared-folder-edit-modal>

    <nfs-shared-folder-edit-modal
      id="modalResetPermissionsSharedFolder"
      action="reset-permissions"
      v-on:modal-close="read"
      v-bind:initial-item="currentItem"
    ></nfs-shared-folder-edit-modal>

    <nfs-shared-folder-edit-modal
      id="modalMigrateSharedFolder"
      action="migrate"
      v-on:modal-close="read"
      v-bind:initial-item="currentItem"
    ></nfs-shared-folder-edit-modal>
  </div>
</template>

<script>
import execp from "@/execp";
import NfsSharedFoldersListView from "@/components/NfsSharedFoldersListView.vue";
import NfsSharedFolderEditModal from "@/components/NfsSharedFolderEditModal.vue";

export default {
  name: "NfsSharedFolders",
  components: {
    NfsSharedFoldersListView,
    NfsSharedFolderEditModal
  },
  beforeRouteLeave(to, from, next) {
    $(".modal").modal("hide");
    next();
  },
  mounted() {
    this.read();
  },
  data() {
    return {
      vReadStatus: "running",
      vReadError: "",
      accountsProvider: "",
      sharedfolders: [],
      currentItem: {},
      groups: [],
      lastDate: null
    };
  },
  methods: {
    createSharedFolder() {
      return {
        Description: "",
        OwningGroup: "",
        SmbRecycleBinStatus: "disabled",
        SmbRecycleBinVersionsStatus: "disabled",
        SmbShareBrowseable: "enabled",
        acls: { EVERYONE: this.accountsProvider == "ad" ? "" : "rw" },
        name: "",
        guestAccess: "disabled",
        SmbAuditStatus: "disabled"
      };
    },
    openModal(id, item) {
      this.currentItem = Object.assign(this.createSharedFolder(), item);
      window.jQuery("#" + id).modal();
    },
    read(eventData = {}) {
      this.vReadStatus = "running";
      execp("nethserver-nfs/sharedfolders/read", { action: "list" })
        .then(result => {
          this.sharedfolders = result.sharedfolders;
          this.accountsProvider = result.accountsProvider;
          this.groups = result.groups;
          this.lastDate = result.date;
          this.vReadStatus = "success";

          this.$nextTick(function() {
            $("[data-toggle=popover]")
              .popovers()
              .on("hidden.bs.popover", function(e) {
                $(e.target).data("bs.popover").inState.click = false;
              });
          });
        })
        .catch(error => {
          this.vReadStatus = "error";
          this.vReadError = error;
        });
    }
  }
};
</script>