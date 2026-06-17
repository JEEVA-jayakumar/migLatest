<template>
  <q-page>
    <div class="capitalize">
      <q-pull-to-refresh :distance="30" @refresh="PullToRefresh">
        <generalLeadInformation
          v-if="propToggleLeadInformation"
          :leadInformation="addtnLeadInformation"
          :propToggleLeadInformationPop="propToggleLeadInformation"
          @closeLeadInformation="toggleLeadInformation"
        />
        <div class="col-md-12 q-title q-px-lg q-py-md text-weight-regular bottom-border text-grey-9">
          Bijlipay Open Merchant Tracker/Lead Tracker
        </div>
        <q-table
          table-class="customTableClass"
          :rows="tableData"
          :columns="columns"
          :filter="filter"
          v-model:pagination="paginationControl"
          row-key="id"
        >
          <template v-slot:body-cell-createdAt="props">
            <q-td v-if="props.row" :props="props">
              <span class="label">{{ $moment(props.row.createdAt).format("Do MMM Y") }}</span>
            </q-td>
          </template>
          <template v-slot:body-cell-submitteSATDate="props">
            <q-td v-if="props.row" :props="props">
              <span class="label">{{ $moment(props.row.submitteSATDate).format("Do MMM Y") }}</span>
            </q-td>
          </template>
          <template v-slot:body-cell-applicationNumber="props">
            <q-td v-if="props.row" :props="props">
              <span class="label capitalize">{{ props.row.applicationNumber }}</span>
            </q-td>
          </template>
          <template v-slot:body-cell-leadName="props">
            <q-td v-if="props.row" :props="props">
              <span class="label capitalize">{{ props.row.leadName }}</span>
            </q-td>
          </template>
          <template v-slot:body-cell-leadNumber="props">
            <q-td class="cursor-pointer" @click="toggleLeadInformation(props.row)" v-if="props.row" :props="props">
              <span class="label text-primary"># {{ props.row.leadNumber }}</span>
            </q-td>
          </template>
          <template v-slot:body-cell-createdBy="props">
            <q-td v-if="props.row" :props="props">
              <span class="label">{{ props.row.createdBy ? (props.row.createdBy.name + " | " + props.row.createdBy.employeeID) : "NA" }}</span>
            </q-td>
          </template>
          <template v-slot:body-cell-leadAddress="props">
            <q-td v-if="props.row" :props="props">
              <span class="label">{{ props.row.leadAddress }}</span>
            </q-td>
          </template>
          <template v-slot:body-cell-verifiedStatus="props">
            <q-td v-if="props.row" :props="props">{{ props.row.verifiedStatus }}</q-td>
          </template>

          <template v-slot:top>
            <div class="col-5">
              <q-input dense clearable v-model="filter" color="grey-9" placeholder="Type.." label="Search by Merchant Name, Lead ID" class="q-mr-lg q-py-sm">
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
            <div class="col-md-7">
              <downloadExcel :data="excelTableData" :fields="excelColumnData_field" name="Merchant Transaction Level.xls">
                <q-btn outline color="grey-9" label="Download as Excel" class="q-mr-lg q-py-sm float-right" size="md" />
              </downloadExcel>
            </div>
          </template>
        </q-table>
      </q-pull-to-refresh>
      <div v-if="getToggleCommonLoader" class="fullscreen spinner-overlay">
        <q-spinner-bars class="absolute-center" style="color:#61116a" :size="35"/>
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import generalLeadInformation from "../../components/generalLeadInformation.vue";

export default {
  name: "openMerchantTracker",
  components: {
    generalLeadInformation
  },
  data: () => ({
    propToggleLeadInformation: false,
    addtnLeadInformation: null,
    paginationControl: {
      rowsPerPage: 10,
      page: 1,
      rowsNumber: 0
    },
    filter: "",
    columns: [
      { name: "createdAt", required: true, label: "Created Date", align: "left", field: "createdAt", sortable: true },
      { name: "submitteSATDate", required: true, label: "Submitted Date", align: "center", field: "submitteSATDate", sortable: true },
      { name: "applicationNumber", required: true, label: "MRL app no", align: "left", field: row => "# " + (row.applicationNumber || "NA"), sortable: true },
      { name: "leadNumber", required: true, label: "Lead ID", align: "left", field: row => "# " + row.leadNumber, sortable: true },
      { name: "leadName", required: true, label: "Merchant Name", align: "left", field: "leadName", sortable: false },
      { name: "leadAddress", required: true, label: "Location", align: "left", field: "leadAddress", sortable: false },
      { name: "createdBy", required: true, label: "SO Name", align: "left", field: "createdBy", sortable: false },
      { name: "verifiedStatus", required: true, label: "Status", align: "left", field: "verifiedStatus", sortable: false }
    ],
    excelColumnData_field: {
      "Created Date": "createdAt",
      "Submitted Date": "submitteSATDate",
      "Lead ID": "id",
      "State": "state",
      "SO Name": "soName",
      "Status": "verifiedStatus"
    },
    excelTableData: [],
    tableData: [],
  }),
  created() {
    this.ajaLoadDataAllopenAggMerchantTrackerData();
  },
  computed: {
    ...mapGetters("OpenMerchantTracker", ["getAggOpenMerchantTracker"]),
    ...mapGetters("commonLoader", ["getToggleCommonLoader"]),
  },
  methods: {
    ...mapActions("OpenMerchantTracker", ["FETCH_ALL_AGG_OPEN_MERCHANT_TRACKER_DATA"]),
    ...mapActions("commonLoader", ["TOGGLE_COMMON_LOADER"]),
    ajaLoadDataAllopenAggMerchantTrackerData() {
      this.TOGGLE_COMMON_LOADER(true);
      this.FETCH_ALL_AGG_OPEN_MERCHANT_TRACKER_DATA()
        .then(() => {
          this.tableData = this.getAggOpenMerchantTracker || [];
          this.prepareExcelData();
        })
        .catch(error => {
          console.error("OpenMerchantTracker Load Error:", error);
        })
        .finally(() => {
          this.TOGGLE_COMMON_LOADER(false);
        });
    },
    prepareExcelData() {
      const data = this.getAggOpenMerchantTracker || [];
      this.excelTableData = data.map(value => ({
        createdAt: value.createdAt,
        submitteSATDate: value.submitteSATDate,
        id: value.id,
        state: value.state,
        soName: value.createdBy ? value.createdBy.name : "NA",
        verifiedStatus: value.verifiedStatus
      }));
    },
    toggleLeadInformation(leadDetails) {
      this.propToggleLeadInformation = !this.propToggleLeadInformation;
      if (leadDetails != undefined) {
        this.addtnLeadInformation = leadDetails;
      }
    },
    PullToRefresh(done) {
      this.FETCH_ALL_AGG_OPEN_MERCHANT_TRACKER_DATA()
        .then(() => {
          this.tableData = this.getAggOpenMerchantTracker;
          this.prepareExcelData();
          if (done) done();
        })
        .catch(() => {
          if (done) done();
        });
    }
  }
};
</script>

<style>
</style>
