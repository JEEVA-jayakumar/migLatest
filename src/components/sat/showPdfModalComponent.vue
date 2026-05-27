<template>
  <div>
    <q-dialog
      @hide="emitToggleRemarks"
      v-model="toggleModal"
    >
      <q-card style="min-width: 80vw; min-height: 80vh;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Document Viewer</div>
          <q-spacer />
          <q-btn icon="close" flat round dense v-close-popup @click="emitToggleRemarks" />
        </q-card-section>

        <q-separator />

        <q-card-section class="q-pa-md scroll" style="max-height: 70vh">
          <div class="full-width">
            <vuePdfjs
              :url="GLOBAL_FILE_FETCH_URL+'/'+itemDetail"
              :type="0"
              :height="'600px'"
              style="max-width:100%"
            ></vuePdfjs>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import vuePdfjs from "vue-pdfjs";
import { mapGetters, mapActions } from "vuex";

export default {
  components: {
    vuePdfjs
  },
  props: ["propToggleshowPDFModal", "propPDFDetails"],
  data() {
    return {
      toggleModal: this.propToggleshowPDFModal,
      itemDetail: this.propPDFDetails
    };
  },
  computed: {
    ...mapGetters("GlobalVariables", ["GLOBAL_FILE_FETCH_URL"])
  },
  methods: {
    emitToggleRemarks() {
      this.$emit("togglePDFModal");
    }
  }
};
</script>
<style>
.no-underline {
  text-decoration: none;
}
</style>
 