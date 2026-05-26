<template>
  <q-dialog
    maximized
    persistent
    :model-value="true"
  >
    <q-card class="column full-height">

      <!-- Sticky Header with close button — always visible -->
      <q-card-section class="row items-center q-px-lg q-py-md text-weight-regular bottom-border text-grey-9 bg-white" style="flex-shrink:0">
        <div class="col text-h6">Lead Details</div>
        <div class="col-auto">
          <q-btn round flat icon="clear" color="dark" @click="emitToggleRemarks" />
        </div>
      </q-card-section>

      <q-separator />

      <!-- Scrollable content area -->
      <q-card-section class="col q-pa-none" style="overflow-y:auto">

        <!-- Common lead information in popup -->
        <generalLeadInformation
          v-if="propToggleLeadInformation"
          :leadInformation="addtnLeadInformation"
          :propToggleLeadInformationPop="propToggleLeadInformation"
          @closeLeadInformation="toggleLeadInformation"
        />

        <!-- table lead validation -->
        <q-table
          title="Lead Validation"
          table-class="customTableClass"
          class="q-py-none"
          :rows="tableData"
          :columns="columns"
          :filter="filter"
          v-model:pagination="paginationControl"
          :rows-per-page-options="[5,10,15,20]"
          @request="ajaxLoadAllLeadInfo"
          row-key="nam6"
        >
          <template v-slot:body-cell-createdAt="props">
            <q-td :props="props">{{ $moment(props.row.date).format("Do MMM Y") }}</q-td>
          </template>

          <template v-slot:body-cell-leadNumber="props">
            <q-td :props="props" class="cursor-pointer" @click="toggleLeadInformation(props.row)">
              <span
                class="label"
                :class="[props.row.priority ? 'text-negative text-weight-bolder' : 'text-primary']"
              ># {{props.row.leadNumber}}</span>
            </q-td>
          </template>

          <template v-slot:body-cell-leadName="props">
            <q-td :props="props">
              <span class="capitalize">{{props.row.merchantName}}</span>
            </q-td>
          </template>

          <template v-slot:body-cell-state="props">
            <q-td :props="props">
              <span class="capitalize">{{props.row.state}}</span>
            </q-td>
          </template>

          <template v-slot:body-cell-verifiedFinanceStatus="props">
            <q-td :props="props">
              <span class="label text-positive" v-if="props.row.verifiedFinanceStatus == $VERIFIED_FINANCE_STATUS_SUCCESS">Approved</span>
              <span class="label text-negative" v-else-if="props.row.verifiedFinanceStatus == $VERIFIED_FINANCE_STATUS_PENDING">Pending</span>
              <span class="label text-negative" v-else-if="props.row.verifiedFinanceStatus == $VERIFIED_FINANCE_STATUS_REJECT">Rejected</span>
              <span class="label" v-else>NA</span>
            </q-td>
          </template>

          <template v-slot:body-cell-action="props">
            <q-td :props="props">
              <q-btn
                v-if="props.row.leadStatus == $LEAD_STATUS_DATA_ENTRY_PENDING"
                push outline color="purple-9" size="sm"
                @click="$router.push('/sat/lead/validation/'+ props.row.leadId+'/data/entry')"
              >Data Entry</q-btn>

              <q-btn
                v-else-if="props.row.leadStatus == $LEAD_STATUS_SUBMITED_TO_MARS"
                push disable color="purple-9" size="sm"
              >Pending with MARS</q-btn>

              <q-btn
                v-else-if="props.row.leadStatus == $LEAD_STATUS_SUBMIT_TO_SAT_LEAD && props.row.verifiedFinanceStatus == $VERIFIED_FINANCE_STATUS_SUCCESS"
                push outline color="purple-9" size="sm"
                :to="'/sat/lead/validation/'+ props.row.leadId"
              >Validate</q-btn>

              <q-btn v-else disable push outline color="grey-9" size="sm">Validate</q-btn>
            </q-td>
          </template>

          <template v-slot:top>
            <div class="col-md-5">
              <q-input
                clearable
                color="grey-9"
                v-model="filter"
                :debounce="600"
                placeholder="Type.."
                label="Search .. "
                class="q-mr-lg q-py-sm"
              />
            </div>
          </template>
        </q-table>

      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { useQuasar } from "quasar";
import generalLeadInformation from "../generalLeadInformation.vue";

export default {
  name: "leadValidation",
  props: ["propLeadInformation", "propToggleModal"],
  components: {
    generalLeadInformation
  },
  setup() {
    const $q = useQuasar();
    return { $q };
  },
  data() {
    return {
      propToggleLeadInformation: false,
      addtnLeadInformation: null,
      filter: "",
      toggleAjaxLoadFilter: false,
      paginationControl: {
        rowsNumber: 10,
        page: 1,
        sortBy: "leadNumber",
        descending: false
      },
      columns: [
        { name: "createdAt", required: true, label: "Date(C)", align: "left", field: "date", sortable: true },
        { name: "leadNumber", required: true, label: "Lead ID", align: "center", field: row => "# " + row.leadNumber, sortable: true },
        { name: "leadName", required: true, label: "Merchant Name", align: "left", field: "merchantName", sortable: true },
        { name: "state", required: true, label: "State", align: "left", field: "state", sortable: true },
        { name: "assignedTo.name", required: true, label: "SO Name", align: "left", field: "salesOfficerName", sortable: true },
        {
          name: "verifiedFinanceStatus",
          required: true,
          label: "Finance Approval",
          align: "left",
          field: row => {
            return row.verifiedFinanceStatus == this.$VERIFIED_FINANCE_STATUS_SUCCESS ? "Success"
              : row.verifiedFinanceStatus == this.$VERIFIED_FINANCE_STATUS_PENDING ? "Pending"
              : row.verifiedFinanceStatus == this.$VERIFIED_FINANCE_STATUS_REJECT ? "Rejected"
              : "NA";
          },
          sortable: true
        },
        { name: "action", required: true, label: "", align: "left", field: "action", sortable: false }
      ],
      loading: true,
      tableData: []
    };
  },
  computed: {
    ...mapGetters("SAT_Dashboard", ["getSatAgingTrackerListdata"])
  },
  mounted() {
    this.ajaxLoadAllLeadInfo({
      pagination: this.paginationControl,
      filter: this.filter
    });
  },
  methods: {
    ...mapActions("SAT_Dashboard", ["FETCH_SAT_AGING_TRACKER_LEADS_DATA"]),

    ajaxLoadAllLeadInfo({ pagination, filter }) {
      this.tableData = [];
      this.$q.loading.show({ delay: 0, spinnerColor: "purple-9", message: "Fetching data .." });
      this.FETCH_SAT_AGING_TRACKER_LEADS_DATA({
        pagination: pagination,
        filter: filter,
        leadIdList: { leadIdList: this.propLeadInformation }
      })
        .then(() => {
          this.paginationControl = pagination;
          this.paginationControl.rowsNumber = this.getSatAgingTrackerListdata.totalElements;
          this.paginationControl.page = this.getSatAgingTrackerListdata.number + 1;
          this.tableData = this.getSatAgingTrackerListdata.content;
          if (this.getSatAgingTrackerListdata.sort != null) {
            this.paginationControl.sortBy = this.getSatAgingTrackerListdata.sort[0].property;
            this.paginationControl.descending = this.getSatAgingTrackerListdata.sort[0].ascending;
          }
          this.toggleAjaxLoadFilter = false;
          this.$q.loading.hide();
        })
        .catch(() => {
          this.toggleAjaxLoadFilter = false;
          this.$q.loading.hide();
        });
    },

    toggleLeadInformation(leadDetails) {
      this.propToggleLeadInformation = !this.propToggleLeadInformation;
      if (leadDetails != undefined) {
        this.addtnLeadInformation = leadDetails;
      }
    },

    emitToggleRemarks() {
      this.$emit("closeLeadsList");
    }
  }
};
</script>

<style scoped>
.bottom-border {
  border-bottom: 1px solid #e0e0e0;
}
</style>