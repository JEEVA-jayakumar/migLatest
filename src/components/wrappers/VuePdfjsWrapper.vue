<template>
  <div class="vue-pdf-wrapper">
    <vue-pdf-embed :source="url" :height="height" @rendered="handleRendered" @loading-failed="handleError" />
    <div v-if="loading" class="text-center q-pa-md">
      <q-spinner color="primary" size="3em" />
      <div class="q-mt-sm">Loading PDF...</div>
    </div>
    <div v-if="error" class="text-negative text-center q-pa-md">
      <q-icon name="warning" size="3em" />
      <div class="q-mt-sm">Failed to load PDF. It might be blocked by CORS or the file might be missing.</div>
      <div class="text-caption">{{ url }}</div>
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
      loading: true,
      error: false
    }
  },
  methods: {
    handleRendered() {
      this.loading = false;
      this.error = false;
    },
    handleError(err) {
      console.error('PDF loading failed:', err);
      this.loading = false;
      this.error = true;
    }
  }
}
</script>

<style scoped>
.vue-pdf-wrapper {
  min-height: 200px;
  position: relative;
}
</style>
