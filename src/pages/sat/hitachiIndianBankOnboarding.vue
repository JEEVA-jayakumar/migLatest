<template>
  <q-page>
    <!-- CARD 1: Upload Section -->
    <q-card>
      <div class="text-grey-9">
        <div class="row bottom-border q-pa-sm items-center">
          <div class="col">
            <!-- Upload tab header — styled to match q-tabs look -->
            <div class="shadow-1 q-tabs row no-wrap items-center" style="background: #fff;">
              <div class="q-tab size1 q-tab--active text-primary flex flex-center q-pa-sm text-weight-medium" style="font-size:12px; border-bottom: 2px solid #1976d2; min-height:48px;">
                UPLOAD CSV FILE
              </div>
            </div>

            <!-- Upload content directly below, no tab-panels wrapper -->
            <div class="q-pa-md">
              <div class="row text-center justify-center">
                <div class="col-12 q-py-md flex flex-center column">

                  <!-- Drop zone: centered, fixed size, dashed border -->
                  <div
                    v-if="formData.fileSelected.length == 0"
                    :class="[uploaderHovered ? 'toggleBulkUploadDisable' : 'toggleBulkUploadActive']"
                    class="drop flex flex-center cursor-pointer"
                    style="width:100%; max-width:600px; min-height:120px; padding:30px; background-color:#f6f6f6; border-radius:2px; text-align:center;"
                    @dragover.prevent="dragAndDropCustomAnimate(true)"
                    @dragleave.prevent="dragAndDropCustomAnimate(false)"
                    @drop="onDrop"
                  >
                    <label style="width:100%; cursor:pointer; display:block;">
                      Drag & Drop Or Click Here To Open A File
                      <input
                        type="file"
                        name="image"
                        @change="onChange"
                        ref="deviceBulkUpload"
                        accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                        style="position:absolute; opacity:0; z-index:-1;"
                      />
                    </label>
                  </div>

                  <!-- File info card after file selected -->
                  <div v-else style="width:100%; max-width:600px; text-align:left;">
                    <div class="file-card">
                      <div class="file-card__title">Uploaded File</div>
                      <hr class="file-card__sep" />
                      <div class="file-card__body">
                        <svg class="file-card__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="rgba(0,0,0,0.54)"><path d="M16.5 6v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5c0-1.38 1.12-2.5 2.5-2.5s2.5 1.12 2.5 2.5v10.5c0 .55-.45 1-1 1s-1-.45-1-1V6H10v9.5c0 1.38 1.12 2.5 2.5 2.5s2.5-1.12 2.5-2.5V5c0-2.21-1.79-4-4-4S7 2.79 7 5v12.5c0 3.04 2.46 5.5 5.5 5.5s5.5-2.46 5.5-5.5V6h-1.5z"/></svg>
                        <span class="file-card__name">{{ formData.fileSelected[0].name }}</span>
                      </div>
                      <hr class="file-card__sep" />
                      <div class="file-card__actions">
                        <q-btn size="sm" type="button" color="negative"
                          @click="removeBulkUploadFile" label="Remove" icon="clear" />
                      </div>
                    </div>
                  </div>

                </div>

                <div class="col-12 group q-pb-md" align="center">
                  <q-btn
                    :disabled="formData.fileSelected.length == 0 ? true : false"
                    type="button"
                    color="purple-9"
                    label="Submit"
                    @click="uploadFileForBulkUpload"
                  />
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </q-card>

    <!-- CARD 2: Table Section -->
    <q-card class="q-mt-md">
      <div class="text-grey-9">
        <div class="row bottom-border q-pa-sm items-center">
          <div class="col">
            <!-- Table tab header -->
            <div class="shadow-1 q-tabs row no-wrap items-center" style="background: #fff;">
              <div class="q-tab size1 q-tab--active text-primary flex flex-center q-pa-sm text-weight-medium" style="font-size:12px; border-bottom: 2px solid #1976d2; min-height:48px;">
                Hitachi Onboarding Merchants
              </div>
            </div>

            <!-- Table directly below header -->
            <q-table
              :rows="tableData1"
              :columns="columnData"
              table-class="customTableClass"
              :filter="filterSearch1"
              v-model:pagination="paginationControl1"
              row-key="id"
              :loading="tableAjaxLoading1"
              :rows-per-page-options="[5, 10, 15, 20]"
              color="dark"
              @request="ajaxLoadAllLeadInfo1"
            >
              <template v-slot:body-cell-tid="props">
                <q-td :props="props" class="customTd">
                  <div class="text-primary">{{ props.row.tid }}</div>
                </q-td>
              </template>
              <template v-slot:body-cell-mid="props">
                <q-td :props="props" class="customTd">
                  <div class="text-primary">{{ props.row.mid }}</div>
                </q-td>
              </template>
              <template v-slot:body-cell-createdAt="props">
                <q-td :props="props">
                  {{ $moment(props.row.createdAt).format("Do MMM Y") }}
                </q-td>
              </template>
              <template v-slot:body-cell-assign="props">
                <q-td :props="props">
                  <q-btn class="btn1" v-if="props.row.isStatus == 1" disable highlight push color="positive" size="sm">Success</q-btn>
                  <q-btn v-if="props.row.isStatus == 2" highlight push color="negative" size="sm" @click="OGSPendingStatus(props.row)">Re-Submit</q-btn>
                  <q-btn v-if="props.row.isStatus == 3" highlight push color="negative" size="sm" @click="OGSPendingStatus(props.row)">Re-Submit</q-btn>
                  <q-btn class="btn1" v-if="props.row.isStatus == 4" disable highlight push color="purple-9" size="sm">Installed</q-btn>
                  <q-btn v-if="props.row.isStatus == null" highlight push color="purple-9" size="sm" @click="OGSPendingStatus(props.row)">Re-Submit</q-btn>
                </q-td>
              </template>
              <template v-slot:top>
                <div class="col-md-4">
                  <q-input clearable color="grey-9" v-model="filterSearch1" placeholder="Type.."
                    label="Search by MerchantName, TID, MID..." class="q-mr-lg q-py-sm" />
                </div>
                <div class="col-md-6">
                  <q-btn color="purple-9" label="Download as Excel"
                    class="q-mr-lg q-py-sm float-right" size="md" @click="downloadHitachiIndianBank()" />
                </div>
              </template>
            </q-table>

            <div class="row items-center gutter-y-sm">
              <div class="col-md-9 col-sm-12 col-xs-12">
                <div class="row items-center"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </q-card>

    <downloadIndianBankReports
      v-if="propHitachiReport"
      :propHitachiReport="propHitachiReport"
      @emitfnHitachiIndianBank="downloadHitachiIndianBank"
    ></downloadIndianBankReports>
  </q-page>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import downloadIndianBankReports from "../../components/sat/downloadIndianBankReports.vue";

export default {
  name: "hitachiIndianBankOnboarding",
  components: { downloadIndianBankReports },
  data() {
    return {
      propToggleLeadInformation: false,
      propHitachiReport: false,
      addtnLeadInformation: null,
      filterSearch: "",
      filterSearch1: "",
      selectedTab: "unAssigned",
      assignTo: "",
      assignToOptions: [],
      tableData: [],
      tableData1: [],
      uploaderHovered: false,
      currentDeviceInfo: {},
      showDeviceAddressModal: false,
      columnData: [
        { name: "createdAt", required: true, label: "Upload Date / Time", align: "left", field: row => row.createdAt, format: val => `${val}|moment("Do MMM Y")`, sortable: true },
        { name: "merchant_name", required: true, label: "Merchant Name", align: "left", field: row => row.leadName == null ? "NA" : row.leadName, sortable: false },
        { name: "tid", required: true, label: "TID", align: "left", field: row => row.tid, sortable: false },
        { name: "mid", required: true, label: "MID", align: "left", field: row => row.mid, sortable: false },
        { name: "device_model", required: true, label: "Device Model", align: "center", field: row => row.device != null ? row.device : "NA", sortable: false },
        { name: "device_address", required: true, label: "Contact Name", align: "left", field: row => row.contactName == null ? "NA" : row.contactName, sortable: false },
        { name: "contact_number", required: true, label: "Contact Number", align: "center", field: row => row.contactNumber != null ? row.contactNumber : "NA", sortable: false },
        { name: "status", required: true, label: "Status", align: "left", field: row => {
          if (row.isStatus == 1) return "Success";
          else if (row.isStatus == 2) return "Pending";
          else if (row.isStatus == 3) return "OGS Failure";
          else if (row.isStatus == 4) return "Installed";
          else return "Failure";
        }, sortable: false },
        { name: "assign", required: true, label: "Action", align: "left", field: "action", sortable: false }
      ],
      formData: {
        marsDeviceIdsCooked: [],
        marsDeviceIdsCookedUnAssinged: [],
        triggerWelcomeMail: false,
        assignTo: "",
        fileSelected: []
      },
      paginationControl: { sortBy: "createdAt", descending: false, page: 1, rowsPerPage: 5 },
      paginationControl1: { sortBy: "createdAt", descending: false, page: 1, rowsPerPage: 5 },
      tableAjaxLoading: false,
      tableAjaxLoading1: false
    };
  },
  computed: {
    ...mapGetters("HitachiIndianBankOnboarding", ["getHitachiIndianOnboarding"])
  },
  beforeMount() {
    console.log("FORMDATA------------->>>>", JSON.stringify(this.formData.props));
    console.log("PROPS DETAILS TID1-------------->>>>", JSON.stringify(this.props));
  },
  mounted() {
    console.log("File Selected--------->>>>", JSON.stringify(this.formData.fileSelected));
    this.ajaxLoadAllLeadInfo1({ pagination: this.paginationControl1, filter: this.filterSearch1 });
  },
  methods: {
    ...mapActions("HitachiIndianBankOnboarding", ["HITACHI_INDIAN_ONBOARDING_LIST", "REASSIGN_HITACHI_MERCHANTS"]),
    ...mapActions("InventoryCentral", ["REPORT_HITACHI_ONBOARDING_MERCHANTS"]),
    ...mapActions("SuperAdminUsers", ["FETCH_ALL_STATES_DATA"]),
    ...mapActions("IndianBankUpload", ["FEED_HITACHI_INDIAN_BANK_ONBOARDING_UPLOAD_DATA"]),

    removeBulkUploadFile() { this.formData.fileSelected = []; },
    dragAndDropCustomAnimate(action) { this.uploaderHovered = action; },
    onDrop(e) {
      e.stopPropagation(); e.preventDefault();
      this.formData.fileSelected = e.dataTransfer.files;
      this.fileCheckSum(e.dataTransfer.files);
    },
    fileCheckSum(file) {
      console.log(file);
      let re = /(\.csv|\.xlsx|\.xls)$/i;
      if (!re.exec(file[0].name)) {
        this.formData.fileSelected = [];
        this.$q.notify({ color: "negative", position: "bottom", message: "File format not supported", icon: "clear" });
        return false;
      }
    },
    onChange(e) { this.formData.fileSelected = e.target.files; },
    uploadFileForBulkUpload() {
      this.$q.loading.show({ delay: 0, spinnerColor: "purple-9", message: "Validating .." });
      if (this.formData.fileSelected.length == 0) {
        this.$q.notify({ color: "amber-9", position: "bottom", message: "Please upload file", icon: "warning" });
        return false;
      } else {
        this.$q.loading.show({ delay: 100, spinnerColor: "purple-9", message: "Please wait.." });
        let assumeFormData = new FormData();
        assumeFormData.append("file", this.formData.fileSelected[0]);
        let assumeFormDataValue = { file: assumeFormData };
        this.FEED_HITACHI_INDIAN_BANK_ONBOARDING_UPLOAD_DATA(assumeFormDataValue)
          .then(response => {
            this.$q.loading.hide();
            this.$q.notify({ color: "positive", position: "bottom", message: "Successfully Uploaded!", icon: "thumb_up" });
            this.ajaxLoadAllLeadInfo1({ pagination: this.paginationControl, filter: this.filterSearch });
            this.$emit("emitToggleinventoryBulkUploadOnSuccess");
            this.formData.fileSelected = [];
          })
          .catch(error => {
            this.$q.loading.hide();
            this.$q.notify({ color: "negative", position: "bottom", message: error.body.message == null ? "Please Try Again Later !" : error.body.message, icon: "thumb_down" });
          });
      }
    },
    getPincodeInformations() { this.FETCH_ALL_STATES_DATA(); },
    ajaxLoadAllLeadInfo1({ pagination, filter }) {
      this.$q.loading.show({ delay: 0, spinnerColor: "purple-9", message: "Fetching data .." });
      this.HITACHI_INDIAN_ONBOARDING_LIST({ pagination, filter })
        .then(res => {
          this.paginationControl1 = pagination;
          this.paginationControl1.rowsNumber = this.getHitachiIndianOnboarding.totalElements;
          this.paginationControl1.page = this.getHitachiIndianOnboarding.number + 1;
          this.tableData1 = this.getHitachiIndianOnboarding.content;
          if (this.getHitachiIndianOnboarding.sort != null) {
            this.paginationControl1.sortBy = this.getHitachiIndianOnboarding.sort[0].property;
            this.paginationControl1.descending = this.getHitachiIndianOnboarding.sort[0].ascending;
          } else {
            this.paginationControl1.sortBy = "createdAt";
            this.paginationControl1.descending = !this.paginationControl1.descending;
          }
          this.$q.loading.hide();
        })
        .catch(() => { this.$q.loading.hide(); });
    },
    goToUnassignedTab(tab) {
      this.ajaxLoadAllLeadInfo1({ pagination: this.paginationControl1, filter: this.filterSearch1 });
    },
    UpdateDeviceAddress(currentDeviceInfo) {
      this.currentDeviceInfo = [];
      this.showDeviceAddressModal = !this.showDeviceAddressModal;
      if (this.formData.marsDeviceIdsCooked.length == 0) {
        this.currentDeviceInfo = { id: [currentDeviceInfo.id], marsDeviceAddress: { deviceAddress: currentDeviceInfo.deviceAddress, latitude: 0, longitude: 0, pincode: currentDeviceInfo.pincode, city: currentDeviceInfo.city, state: currentDeviceInfo.state } };
      } else {
        let marsDeviceIdsCooked = [];
        this.formData.marsDeviceIdsCooked.map(function(value) { marsDeviceIdsCooked.push(value.id); });
        this.currentDeviceInfo = { id: marsDeviceIdsCooked, marsDeviceAddress: { deviceAddress: currentDeviceInfo.deviceAddress, latitude: 0, longitude: 0, pincode: currentDeviceInfo.pincode, city: currentDeviceInfo.city, state: currentDeviceInfo.state } };
      }
    },
    UpdateDeviceAddressAfterEmit(pagination) {
      this.showDeviceAddressModal = !this.showDeviceAddressModal;
      this.paginationControl = pagination;
    },
    OGSPendingStatus(request) {
      console.log("PROPS DETAILS TID STATUS-------->>>>", JSON.stringify(request.tid));
      let param = { tid: request.tid };
      this.$q.loading.show({ delay: 100, message: "Please Wait", spinnerColor: "purple-9", customClass: "shadow-none" });
      this.REASSIGN_HITACHI_MERCHANTS(param)
        .then(response => {
          this.ajaxLoadAllLeadInfo1({ pagination: this.paginationControl1, filter: this.filterSearch1 });
          this.$q.notify({ color: "positive", position: "bottom", message: "Re-Assigned Successfully", icon: "thumb_up" });
          this.$q.loading.hide();
        })
        .catch(error => {
          this.$q.loading.hide();
          this.$q.notify({ color: "negative", position: "bottom", message: error.body.message == null ? "Please Try Again Later !" : error.body.message, icon: "thumb_down" });
        });
    },
    downloadHitachiIndianBank() { this.propHitachiReport = !this.propHitachiReport; },
    toggleLeadInformation(leadDetails) {
      this.propToggleLeadInformation = !this.propToggleLeadInformation;
      if (leadDetails != undefined) { this.addtnLeadInformation = leadDetails; }
    }
  }
};
</script>

<style scoped>
.customTd { text-align: left !important; word-wrap: break-word; white-space: normal; }
.customTd.customCellLength { min-width: 300px !important; overflow-x: auto; }
* { font-family: "Arial"; font-size: 12px; }
.btn1 { width: 87px; }
.drop {
  padding: 30px;
  background-color: #f6f6f6;
  border-radius: 2px;
  width: 100%;
  max-width: 600px;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.toggleBulkUploadActive { border: 4px dashed #ccc; }
.toggleBulkUploadDisable { border: 4px dashed #1f2c3fa6; }
/* File info card — plain HTML replicating legacy q-card-title/q-card-main/q-item-side/q-item-main */
.file-card {
  border: 1px solid rgba(0,0,0,0.12);
  border-radius: 4px;
  background: #fff;
}
.file-card__title {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: rgba(0,0,0,0.87);
}
.file-card__sep {
  margin: 0;
  border: none;
  border-top: 1px solid rgba(0,0,0,0.12);
}
.file-card__body {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 8px 16px;
  gap: 8px;
}
.file-card__icon {
  font-size: 20px !important;
  color: rgba(0,0,0,0.54);
  flex-shrink: 0;
  width: 20px;
  height: 20px;
}
.file-card__name {
  font-size: 13px;
  color: rgba(0,0,0,0.87);
  word-break: break-all;
}
.file-card__actions {
  display: flex;
  justify-content: flex-end;
  padding: 4px 8px;
}
</style>