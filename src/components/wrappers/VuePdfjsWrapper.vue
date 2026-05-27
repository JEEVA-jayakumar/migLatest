<template>
  <div class="pdf-viewer-container">
    <vue-pdf-embed
      v-if="url"
      :source="url"
      @rendered="handleRendered"
      @loading="handleLoading"
    />
    <div v-if="loading" class="flex flex-center q-pa-xl">
      <q-spinner color="primary" size="3em" />
    </div>
  </div>
</template>

<script>
import VuePdfEmbed from 'vue-pdf-embed'

export default {
  components: {
    VuePdfEmbed,
  },
  props: ['url', 'height'],
  data() {
    return {
      loading: true
    }
  },
  methods: {
    handleLoading() {
      this.loading = true
    },
    handleRendered() {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.pdf-viewer-container {
  width: 100%;
  min-height: 200px;
}
</style>
