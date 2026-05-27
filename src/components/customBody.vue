<template>
  <router-view v-slot="{ Component, route }">
    <transition
      appear
      @before-enter="beforeEnter"
      @enter="enter"
      @after-enter="afterEnter"
      mode="out-in"
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
    >
      <div :key="route.path" v-if="Component">
        <component :is="Component" />
      </div>
    </transition>
  </router-view>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "CustomBody",
  data() {
    return {
      toggleAjaxLoadFilter: true
    };
  },
  computed: {
    ...mapGetters("commonLoader", ["getToggleCommonLoader"])
  },
  methods: {
    ...mapActions("commonLoader", ["TOGGLE_COMMON_LOADER"]),
    beforeEnter: function(el) {
      this.TOGGLE_COMMON_LOADER(true);
    },
    // the done callback is optional when
    // used in combination with CSS
    enter: function(el, done) {
      done();
    },

    afterEnter: function(el) {
      this.TOGGLE_COMMON_LOADER(false);
    }
  }
};
</script>
