<template>
  <div>
    <q-dialog
      v-model="toggleModel"
      no-backdrop-dismiss
      persistent
      @hide="emitfnReferBackRemarks"
    >
      <q-card style="padding: 30px; min-width: 50vw; max-height: 90vh; overflow-y: auto;">
        <div class="row items-center bottom-border q-py-sm">
          <div class="col">
            <strong>REFERBACK REMARKS</strong>
          </div>
          <div class="col-auto">
            <q-btn round size="sm" @click="emitfnReferBackRemarks" color="red" icon="clear" />
          </div>
        </div>
        <br />

        <div v-if="propRowDetails.qrLeadStatus == 9" class="row d-flex align-items-center">
          <div class="col-sm-4">
            <strong>SAT TO MARS Remark</strong>
          </div>
          <div class="col-sm-8">
            <q-input
              readonly
              v-model="satToSoRemarks"
              type="textarea"
              color="red-12"
              label="Textarea with shadow text"
              hint="Press TAB to autocomplete suggested value or ESC to cancel suggestion"
            />
          </div>
        </div>
        <br />

        <div v-if="propRowDetails.qrLeadStatus == 9" class="row d-flex align-items-center">
          <div class="col-sm-4">
            <strong>MARS Remark</strong>
          </div>
          <div class="col-sm-8">
            <q-input
              readonly
              v-model="marsRemarks"
              type="textarea"
              color="red-12"
              label="Textarea with shadow text"
              hint="Press TAB to autocomplete suggested value or ESC to cancel suggestion"
            />
          </div>
        </div>
        <br />

        <div v-if="propRowDetails.qrLeadStatus == 4 && propRowDetails.referbackStatus == true" class="row d-flex align-items-center">
          <div class="col-sm-4">
            <strong>SAT TO SO Remark</strong>
          </div>
          <div class="col-sm-8">
            <q-input
              readonly
              v-model="satToSoRemarks"
              type="textarea"
              color="red-12"
              label="Textarea with shadow text"
              hint="Press TAB to autocomplete suggested value or ESC to cancel suggestion"
            />
          </div>
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  props: ["propShowUpdateOpenedExternal", "propRowDetails"],
  name: "MDRdetails",
  data() {
    return {
      toggleModel: this.propShowUpdateOpenedExternal,
      satToSoRemarks: "",
      marsRemarks: ""
    };
  },
  beforeMount() {
    console.log("propRowDetails ------->", JSON.stringify(this.propRowDetails.qrLeadStatus));
    this.marsRemarks = this.propRowDetails.marsReason || "NA";
    this.satToSoRemarks = this.propRowDetails.satToMarsRemarks;
    console.log("REFERBACK Remarks marsReason ------->", JSON.stringify(this.marsRemarks));
    console.log("REFERBACK Remarks satTOMarsRemarks ------->", JSON.stringify(this.satToSoRemarks));
  },
  methods: {
    emitfnReferBackRemarks() {
      this.$emit("emitfnshowUpdateOpenedExternal");
    }
  }
};
</script>

<style>
.cardsizealign1 {
  width: 70%;
  max-height: calc(90vh - 38px);
  overflow-y: auto;
}
</style>