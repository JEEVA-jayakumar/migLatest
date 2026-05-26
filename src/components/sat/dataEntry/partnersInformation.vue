<template>
  <div>
    <div
      v-for="(partner, index) in partnersArr"
      :key="index"
      class="row q-my-xs gutter-sm"
      ref="parentElement"
    >
      <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="row group items-center">
          <div class="col">
            <span class="q-pa-sm bg-light text-dark">
              <q-icon name="people"/>
              Partner 0{{parseInt(index)+1}}
            </span>
          </div>
          <div class="col-auto" v-if="partnersArr.length > 1">
            <q-btn round icon="delete" @click="removePartnerFromArr(partner, index)" color="negative"/>
          </div>
        </div>
      </div>
      <div class="col-md-6 col-sm-12 col-xs-12">
        <q-input
          :error="partnerFieldHasError(index, 'name')"
          @blur="v$.partnersArr.$touch()"
          color="grey-9"
          v-model="partnersArr[index].name"
          label="Name*"
          placeholder="Name*"
        />
      </div>
      <div class="col-md-6 col-sm-12 col-xs-12">
        <q-input
          upper-case
          :error="partnerFieldHasError(index, 'pan')"
          @blur="v$.partnersArr.$touch()"
          color="grey-9"
          v-model="partnersArr[index].pan"
          label="Pan*"
          placeholder="Pan*"
        />
      </div>
      <div class="col-md-6 col-sm-12 col-xs-12">
        <q-input
          :error="partnerFieldHasError(index, 'address')"
          @blur="v$.partnersArr.$touch()"
          color="grey-9"
          v-model="partnersArr[index].address"
          label="Address*"
          placeholder="Address*"
        />
      </div>
      <div class="col-md-6 col-sm-12 col-xs-12">
        <q-input
          :error="partnerFieldHasError(index, 'pin')"
          @blur="v$.partnersArr.$touch()"
          color="grey-9"
          type="number"
          v-model="partnersArr[index].pin"
          label="Pincode*"
          placeholder="Pincode*"
        />
      </div>
      <div class="col-md-6 col-sm-12 col-xs-12">
        <q-select
          use-input
          fill-input
          hide-selected
          :error="partnerFieldHasError(index, 'cityRefLabel') || partnerFieldHasError(index, 'cityRefCode')"
          @blur="v$.partnersArr.$touch()"
          color="grey-9"
          v-model="partnersArr[index].cityRefLabel"
          label="City (type min 3 characters)*"
          placeholder="Start typing ..*"
          :options="cityOptionsFiltered"
          @filter="citySearch"
          @update:model-value="obj => partnerCitySelected(obj, index)"
        ></q-select>
      </div>
      <div class="col-md-6 col-sm-12 col-xs-12">
        <q-select
          use-input
          fill-input
          hide-selected
          :error="partnerFieldHasError(index, 'stateRefLabel') || partnerFieldHasError(index, 'stateRefCode')"
          @blur="v$.partnersArr.$touch()"
          color="grey-9"
          v-model="partnersArr[index].stateRefLabel"
          label="State (type min 3 characters)*"
          placeholder="Start typing ..*"
          :options="stateOptionsFiltered"
          @filter="stateSearch"
          @update:model-value="obj => partnerStateSelected(obj, index)"
        ></q-select>
      </div>
      <div class="col-md-6 col-sm-12 col-xs-12">
        <q-input
          :error="partnerFieldHasError(index, 'contactMobile')"
          @blur="v$.partnersArr.$touch()"
          color="grey-9"
          type="tel"
          v-model="partnersArr[index].contactMobile"
          label="Mobile*"
          placeholder="Mobile*"
        />
      </div>
      <div class="col-md-6 col-sm-12 col-xs-12">
        <q-input
          :error="partnerFieldHasError(index, 'contactEmail')"
          @blur="v$.partnersArr.$touch()"
          color="grey-9"
          type="email"
          v-model="partnersArr[index].contactEmail"
          label="Email*"
          placeholder="Email*"
        />
      </div>
    </div>
    <q-stepper-navigation>
      <q-btn color="primary" class="q-ma-xs" icon="check" @click="validate()" label="Continue"/>
      <q-btn
        color="amber-10"
        class="q-ma-xs"
        icon="save"
        label="Save Partial"
        @click="$emit('saveData','partnerInformation',partnersArr)"
      />
      <q-btn color="grey-7" class="q-ma-xs" icon="block" @click="$emit('goBack')" label="Back"/>
      <q-btn
        color="positive float-right"
        @click="addMorePartnersSet"
        class="q-ma-xs"
        icon="add"
        label="Add More"
      />
    </q-stepper-navigation>
    <div class="hidden">{{makePropsReactive}}</div>
  </div>
</template>

<script>
import { useVuelidate } from '@vuelidate/core';

import {
  helpers,
  required,
  requiredIf,
  integer,
  minLength,
  maxLength,
  email
} from "@vuelidate/validators";
const panCard = helpers.regex(
  /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/
);
export default {
  setup() {
    return { v$: useVuelidate() };
  },
  // name: 'ComponentName',
  props: ["cityOptions", "stateOptions", "constitution", "partnerInformation"],
  data() {
    return {
      partnersArr: [],
      cityOptionsFiltered: [],
      stateOptionsFiltered: []
    };
  },
  validations() {
    return {
      partnersArr: {
        required: requiredIf(function() {
          return this.getPartnersVisiblity;
        }),
        $each: helpers.forEach({
          name: { required },
          address: { required },
          pan: {
            required,
            panCard,
            maxLength: maxLength(10),
            minLength: minLength(10)
          },
          pin: {
            required,
            integer,
            minLength: minLength(6),
            maxLength: maxLength(7)
          },
          stateRefCode: { required, integer },
          stateRefLabel: { required },
          cityRefCode: { required, integer },
          cityRefLabel: { required },
          contactMobile: {
            required,
            integer,
            minLength: minLength(10),
            maxLength: maxLength(10)
          },
          contactEmail: { required, email }
        })
      }
    };
  },
  computed: {
    makePropsReactive() {
      this.partnersArr = this.partnerInformation;
    },
    // Checks for value in partners array => Global variable
    getPartnersVisiblity() {
      return this.$PARTNERS_TAB_ENABLED_ITEMS.includes(this.constitution);
    }
  },
  methods: {
    partnerFieldHasError(index, field) {
      if (!this.v$.partnersArr?.$dirty) return false;
      const errors = this.v$.partnersArr?.$each?.$response?.$errors?.[index]?.[field];
      return !!(errors && errors.length > 0);
    },
    COMMON_FILTER_FUNCTION(arraySet, terms) {
      return _.filter(arraySet, function(oo) {
        return oo.label.toLowerCase().includes(terms.toLowerCase());
      });
    },
    citySearch(terms, update, abort) {
      update(() => {
        this.cityOptionsFiltered = this.COMMON_FILTER_FUNCTION(this.cityOptions, terms);
      });
    },
    stateSearch(terms, update, abort) {
      update(() => {
        this.stateOptionsFiltered = this.COMMON_FILTER_FUNCTION(this.stateOptions, terms);
      });
    },

    // Partners city selection
    partnerCitySelected(item, index) {
      if (item && item.label) {
        this.partnersArr[index].cityRefCode = item.value;
        this.partnersArr[index].cityRefLabel = item.label;
      } else {
        this.partnersArr[index].cityRefCode = '';
        this.partnersArr[index].cityRefLabel = '';
      }
    },

    // Partners state selection
    partnerStateSelected(item, index) {
      if (item && item.label) {
        this.partnersArr[index].stateRefCode = item.value;
        this.partnersArr[index].stateRefLabel = item.label;
      } else {
        this.partnersArr[index].stateRefCode = '';
        this.partnersArr[index].stateRefLabel = '';
      }
    },

    addMorePartnersSet() {
      let partnerObj = {
        name: "",
        address: "",
        pan: "",
        pin: "",
        cityRefCode: "",
        cityRefLabel: "",
        stateRefCode: "",
        stateRefLabel: "",
        contactMobile: "",
        contactEmail: ""
      };
      this.partnersArr.push(partnerObj);
    },

    removePartnerFromArr(item, index) {
      this.partnersArr.splice(index, 1);
    },
    validate() {
      this.v$.partnersArr.$touch();
      if (this.v$.partnersArr.$error) {
        this.$q.notify("Please review fields again.");
      } else {
        this.$emit("goNext", "partnerInformation", {
          partnerInformation: this.partnersArr
        });
      }
    }
  }
};
</script>

<style>
</style>
