<template>
  <div>
    <q-dialog
      @hide="emitToggleRemarks"
      @escape-key="emitToggleRemarks"
      v-model="toggleModal"
      persistent
    >
      <q-card style="min-width: 80vw; max-height: 90vh;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Document Viewer</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="emitToggleRemarks" />
        </q-card-section>

        <q-card-section class="q-pa-none" style="height: 75vh; overflow-y: auto;">
          <vuePdfjs
            v-if="itemDetail"
            :url="GLOBAL_FILE_FETCH_URL+'/'+itemDetail"
            style="width: 100%;"
          ></vuePdfjs>
          <div v-else class="text-center q-pa-md">No document path provided</div>
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
 