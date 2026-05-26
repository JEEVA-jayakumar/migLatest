<template>
  <q-dialog
    v-model="dialogVisible"
    @hide="emitToggleReject()"
    persistent
  >
    <q-card style="padding: 50px; min-width: 400px">
      <q-card-section>
        <div align="center" class="q-subheading q-mb-md capitalize">
          {{ propShowRejectLeadComponent.merchantName }}
        </div>
        <div align="center" class="text-light-blue q-title q-mb-md">
          #{{ propShowRejectLeadComponent.leadNumber }}
        </div>

        <div class="col-md-12">
          <q-input
            color="grey-9"
            disable
            v-model="formData.device"
            label="Selected device"
          />
        </div>

        <div class="col-md-12">
          <div align="center" class="col-md-10 text-light-blue q-title q-mb-md">
            Reason Type
          </div>
          <q-radio
            @blur="v$.formData.leadVerificationStatus.reasonType.$touch"
            :error="v$.formData.leadVerificationStatus.reasonType.$error"
            v-model="formData.leadVerificationStatus.reasonType"
            val="Wrong Device Type"
            color="grey-9"
            label="Wrong Device Type"
          />
          <q-radio
            @blur="v$.formData.leadVerificationStatus.reasonType.$touch"
            :error="v$.formData.leadVerificationStatus.reasonType.$error"
            v-model="formData.leadVerificationStatus.reasonType"
            val="Others"
            color="grey-9"
            label="Others"
          />
        </div>

        <q-input
          type="textarea"
          placeholder="Type Your Reason Here...."
          @blur="v$.formData.leadVerificationStatus.reason.$touch"
          :error="v$.formData.leadVerificationStatus.reason.$error"
          class="q-my-md"
          color="grey-9"
          align="left"
          v-model="formData.leadVerificationStatus.reason"
        />

        <q-btn
          color="negative"
          class="q-ma-sm float-right"
          @click="leadRejectSubmit(formData)"
          align="right"
          label="Reject"
        />
        <q-btn
          align="right"
          color="grey-9"
          class="float-right q-ma-sm"
          @click="emitToggleReject()"
        >Cancel</q-btn>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { useVuelidate } from '@vuelidate/core';
import { required } from "@vuelidate/validators";
import { mapGetters, mapActions } from "vuex";

export default {
  props: ["showRejectLeadModel", "propShowRejectLeadComponent"],

  setup() {
    return { v$: useVuelidate() };
  },

  data() {
    return {
      dialogVisible: this.showRejectLeadModel,
      formData: {
        leadInformation: {
          verifiedFinanceStatus: this.propShowRejectLeadComponent.verifiedFinanceStatus
        },
        leadVerificationStatus: {
          status: 0,
          fieldName: "Device",
          reasonType: "",
          reason: ""
        },
        device: "",
        leadId: this.propShowRejectLeadComponent.leadId,
      },
      propLeadInformation: {},
      propsRowDetails: [],
    };
  },

  validations() {
    return {
      formData: {
        leadVerificationStatus: {
          reason: { required },
          reasonType: { required },
        },
      },
    };
  },

  beforeMount() {
    if (this.getShortLeadInfo && this.getShortLeadInfo.device) {
      this.formData.device = this.getShortLeadInfo.device.deviceName;
    }
  },

  created() {
    this.ajaxLoadShortLeadInfo();
  },

  computed: {
    ...mapGetters("SA_Devices", ["getAllDevicesInfo"]),
    ...mapGetters("SatLeadValidation", ["getShortLeadInfo"]),
  },

  methods: {
    ...mapActions("Finance", ["REJECT_LEAD_EXCEPTION"]),
    ...mapActions("commonLoader", ["TOGGLE_COMMON_LOADER"]),
    ...mapActions("SA_Devices", ["FETCH_DEVICES_DATA"]),
    ...mapActions("SatLeadValidation", ["FETCH_SHORT_LEAD_DATA"]),

    emitToggleReject() {
      this.$emit("closeRejectLeadModel");
    },

    ajaxLoadShortLeadInfo() {
      this.FETCH_SHORT_LEAD_DATA(this.propShowRejectLeadComponent.leadId)
        .then(response => {
          this.propLeadInformation = this.getShortLeadInfo;
          if (this.getShortLeadInfo && this.getShortLeadInfo.device) {
            this.formData.device = this.getShortLeadInfo.device.deviceName;
          }
          this.$q.loading.hide();
        })
        .catch(() => {
          this.$q.loading.hide();
        });
    },

    leadRejectSubmit(formData) {
      this.v$.formData.$touch();
      if (this.v$.formData.$error) {
        this.$q.notify("Please review fields again.");
      } else {
        this.$q.dialog({
            title: "Confirm",
            message: "Are you sure want to reject the lead?",
            ok: "Continue",
            cancel: "Cancel"
          })
          .onOk(() => {
            this.$q.loading.show({
              delay: 0,
              spinnerColor: "purple-9",
              message: "Processing .."
            });
            this.REJECT_LEAD_EXCEPTION(formData)
              .then(() => {
                this.$emit("closeRejectLeadModel");
                this.$q.loading.hide();
                this.$q.notify({
                  color: "negative",
                  position: "bottom",
                  message: "Rejected lead #" + formData.leadId,
                  icon: "clear"
                });
                this.$router.push('/sat/lead/validation');
              })
              .catch(error => {
                this.$q.loading.hide();
                this.$emit("closeRejectLeadModel");
                this.$q.notify({
                  color: "negative",
                  position: "bottom",
                  message: (error.response && error.response.data && error.response.data.message) || "Please Try Again Later !",
                  icon: "thumb_down"
                });
              });
          });
      }
    }
  }
};
</script>