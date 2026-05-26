<template>
  <q-page>
    <div class="text-grey-9">
      <div class="row bottom-border q-pa-sm items-center">
        <div class="col">
          <q-tabs class="shadow-1" color="white" align="justify" v-model="shortlead" @update:model-value="goToSelectedTab">
            <q-tab name="shortlead" color="black" label="Short Lead" />
            <q-tab name="wiplead" color="black" label="WIP Lead" />
          </q-tabs>

          <q-tab-panels v-model="shortlead" animated>
            <q-tab-panel name="shortlead" class="q-pa-none">
              <div class="q-pa-md">
                <div class="col-md-6 q-my-md" align="right">
                  <div class="col group"></div>
                </div>
                <div class="col-12 q-title q-my-lg text-weight-regular">
                  Lead Information
                </div>
                <form>
                  <div class="q-px-md">
                    <div class="q-pa-md">
                      <div class="row q-col-gutter-md q-py-sm">
                        <div class="col-md-6">
                          <q-input v-model.trim="formData.leadName" @blur="v$.formData.leadName.$touch"
                            :error="v$.formData.leadName.$error" class="text-weight-regular text-grey-8" color="grey-9"
                            label="*Merchant Name" placeholder="Merchant Name" />
                        </div>
                        <div class="col-md-6">
                          <q-input v-model.trim="formData.contactName" @blur="v$.formData.contactName.$touch"
                            :error="v$.formData.contactName.$error" class="text-weight-regular text-grey-8"
                            label="*Contact Name" placeholder="Contact Name" />
                        </div>
                        <div class="col-md-6">
                          <q-input type="number" onkeydown="javascript: return event.keyCode === 8 ||
                            event.keyCode === 46 ? true : !isNaN(Number(event.key))"
                            v-model.trim="formData.contactNumber" class="text-weight-regular text-grey-8" color="grey-9"
                            @blur="v$.formData.contactNumber.$touch" :error="v$.formData.contactNumber.$error"
                            label="*Contact Number" placeholder="Contact Number" />
                        </div>
                        <div class="col-md-6">
                          <q-input type="number" onkeydown="javascript: return event.keyCode === 8 ||
                             event.keyCode === 46 ? true : !isNaN(Number(event.key))"
                            v-model.trim="formData.alternateContactNumber" class="text-weight-regular text-grey-8"
                            color="grey-9" label="*Alternate Contact Number" placeholder="Alternate Contact Number" />
                        </div>
                        <div class="col-md-6">
                          <q-input v-model.trim="formData.email" @blur="v$.formData.email.$touch"
                            :error="v$.formData.email.$error" class="text-weight-regular text-grey-8" color="grey-9"
                            label="*Mail_Id" placeholder="Mail_Id" />
                        </div>
                        <div class="col-md-6">
                          <q-input v-model.trim="formData.leadAddress" @blur="v$.formData.leadAddress.$touch"
                            :error="v$.formData.leadAddress.$error" class="text-weight-regular text-grey-8"
                            color="grey-9" label="*Merchant Address" placeholder="Merchant Address" />
                        </div>
                        <div class="col-md-6">
                          <q-select
                            :error="v$.formData.pincodeTemp.$error"
                            @blur="fnClrPin"
                            clearable
                            color="grey-9"
                            v-model="formData.pincodeTemp"
                            label="Pincode"
                            placeholder="Pincode"
                            use-input
                            hide-selected
                            fill-input
                            input-debounce="500"
                            :options="pincodeOptionsSearch"
                            @filter="fnPincodeSearch"
                            @update:model-value="pincodeSelected"
                          />
                        </div>
                        <div class="col-md-6">
                          <q-input disable v-model.trim="formData.state" @blur="v$.formData.state.$touch"
                            :error="v$.formData.state.$error" class="text-weight-regular text-grey-8" color="grey-9"
                            label="State" placeholder="State" />
                        </div>
                        <div class="col-md-6">
                          <q-input disable v-model.trim="formData.city" @blur="v$.formData.city.$touch"
                            :error="v$.formData.city.$error" class="text-weight-regular text-grey-8" color="grey-9"
                            label="City/Down" placeholder="City/Down" />
                        </div>
                        <div class="col-md-6">
                          <q-select v-model.trim="formData.region" @blur="v$.formData.region.$touch"
                            :error="v$.formData.region.$error" class="text-weight-regular text-grey-8" color="grey-9"
                            label="Select Region" placeholder="Select Region" :options="dropDown.regionOptions" emit-value map-options />
                        </div>
                        <div class="col-md-6">
                          <q-select v-model.trim="formData.leadSource" @blur="v$.formData.leadSource.$touch"
                            :error="v$.formData.leadSource.$error" class="text-weight-regular text-grey-8"
                            color="grey-9" label="Lead Source" placeholder="Lead Source"
                            :options="dropDown.leadSourceOptions" @update:model-value="getDevice" emit-value map-options />
                        </div>
                        <div class="col-md-6">
                          <q-select v-model.trim="formData.device" @update:model-value="devSelected"
                            :error="v$.formData.device.$error" class="text-weight-regular text-grey-8" color="grey-9"
                            label="Device Type" placeholder="Device Type" :options="dropDown.deviceOptions" emit-value map-options />
                        </div>
                        <div class="col-md-6">
                          <q-option-group inline type="checkbox" :model-value="selectedVas"
                            @update:model-value="handleVasChange" :disable="vasDisableFlag"
                            class="text-weight-regular text-grey-8" color="grey-9" label="VAS"
                            :options="selectBankEnableOptions" />
                        </div>
                        <!-- Legacy uses selectedVas == 'AMEX' (string compare) -->
                        <div v-if="selectedVas.includes('AMEX')" class="col-md-6">
                          <q-input v-model.trim="formData.ownerFirstName" @blur="v$.formData.ownerFirstName.$touch"
                            :error="v$.formData.ownerFirstName.$error" class="text-weight-regular text-grey-8"
                            color="grey-9" label="Owner 1 First Name*" placeholder="Owner 1 First Name*" />
                        </div>
                        <div v-if="selectedVas.includes('AMEX')" class="col-md-6">
                          <q-input v-model.trim="formData.ownerLastName" @blur="v$.formData.ownerLastName.$touch"
                            :error="v$.formData.ownerLastName.$error" class="text-weight-regular text-grey-8"
                            color="grey-9" label="Owner 1 Last Name*" placeholder="Owner 1 Last Name*" />
                        </div>
                        <div v-if="selectedVas.includes('AMEX')" class="col-md-6">
                          <q-input type="date" v-model.trim="formData.ownerDOB" @blur="v$.formData.ownerDOB.$touch"
                            :error="v$.formData.ownerDOB.$error" class="text-weight-regular text-grey-8" color="grey-9"
                            label="Owner 1 DOB*" placeholder="Owner 1 DOB*" />
                        </div>
                        <div class="col-md-6">
                          <q-input v-model.trim="formData.deviceCount" @blur="v$.formData.deviceCount.$touch"
                            :disable="deviceFlag"
                            :error="v$.formData.deviceCount.$error" class="text-weight-regular text-grey-8"
                            color="grey-9" @keydown="nameKeydown($event)" @keyup="trackChange"
                            label="Device Count" placeholder="Device Count" />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="full-width group" align="center">
                    <q-btn size="md" type="button" color="purple-9" @click="fnSubmitBankDetails(formData)">Submit</q-btn>
                  </div>
                </form>
              </div>
            </q-tab-panel>

            <q-tab-panel name="wiplead" class="q-pa-none">
              <div class="q-pa-md">
                <q-table class="my-sticky-header-table" title="Wip Lead Information" :rows="getShortLead || []"
                  :columns="columns" row-key="id">
                  <template v-slot:body-cell-shortleadDate="props">
                    <q-td :props="props">
                      {{ formatDate(props.row.shortleadDate) }}
                    </q-td>
                  </template>
                  <template v-slot:body-cell-update="props">
                    <q-td :props="props">
                      <div class="row no-wrap no-padding">
                        <q-btn dense no-caps no-wrap label="update" icon="far fa-plus-square" size="md"
                          @click="fnShowConvertToSat(props.row)" flat class="text-light-blue"></q-btn>
                      </div>
                    </q-td>
                  </template>
                </q-table>
                <editShortLead v-if="propShowEditShortLead" :propShowEditShortLead="propShowEditShortLead"
                  :propRowDetails="propRowDetails" @emitfnshowEditShortLead="fnShowEditShortLead"></editShortLead>
                <convertToSat
                  v-if="propShowConvertToSat"
                  :propShowConvertToSat="propShowConvertToSat"
                  :propRowDetails="propRowDetails"
                  @emitEditshowConvertToSat="fnShowConvertToSat"
                ></convertToSat>
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { useVuelidate } from '@vuelidate/core';
import editShortLead from '../../components/sat/editShortLead.vue';
import convertToSat from '../../components/sat/convertToSat.vue';
import _ from 'lodash';
import { required, requiredIf, minLength, maxLength, email } from '@vuelidate/validators';
import { mapGetters, mapActions } from 'vuex';

export default {
  setup() {
    return { v$: useVuelidate() };
  },
  name: 'inventoryAllocation',
  components: { editShortLead, convertToSat },
  data() {
    return {
      propShowEditShortLead: false,
      propShowConvertToSat: false,
      vasDisableFlag: false,
      propRowDetails: '',
      shortlead: 'shortlead',
      deviceFlag: false,
      pinSelected: false,
      pincodeOptionsSearch: [],
      selectedVas: [],
      formData: {
        leadName: '',
        contactName: '',
        contactNumber: '',
        alternateContactNumber: '',
        email: '',
        deviceSelected: '',
        leadAddress: '',
        region: '',
        pincode: '',
        pincodeTemp: '',
        state: '',
        city: '',
        leadSource: '',
        device: '',
        vasInstanceMapping: '',
        deviceCount: '',
        ownerFirstName: '',
        ownerLastName: '',
        ownerDOB: '',
        data: ''
      },
      columns: [
        { name: 'leadName', label: 'leadName', field: 'leadName', align: 'center', sortable: true },
        { name: 'leadNumber', label: 'leadNumber', field: 'leadNumber', align: 'center', sortable: true },
        { name: 'contactNumber', label: 'contactNumber', field: 'contactNumber', align: 'center', sortable: true },
        { name: 'shortleadDate', label: 'shortleadDate', field: 'shortleadDate', align: 'center', sortable: true },
        { name: 'update', required: true, label: 'submit to sat', align: 'left', field: 'action', sortable: false }
      ],
      dropDown: {
        deviceOptions: [],
        leadSourceOptions: [],
        regionOptions: [],
      },
      selectBankEnableOptions: []
    };
  },
  validations() {
    return {
      formData: {
        leadName: { required },
        contactName: { required },
        region: { required },
        contactNumber: { required, minLength: minLength(10), maxLength: maxLength(10) },
        email: { email, required },
        leadAddress: { required },
        pincodeTemp: { required, minLength: minLength(6), maxLength: maxLength(6) },
        state: { required },
        city: { required },
        leadSource: { required },
        device: { required },
        ownerFirstName: { required: requiredIf(() => this.selectedVas.includes('AMEX')) },
        ownerDOB: { required: requiredIf(() => this.selectedVas.includes('AMEX')) },
        ownerLastName: { required: requiredIf(() => this.selectedVas.includes('AMEX')) },
        deviceCount: { required }
      }
    };
  },
  computed: {
    ...mapGetters('appDevice', ['getAllAppDevicesInfo']),
    ...mapGetters('Appvas', ['getVasDeviceMapping']),
    ...mapGetters('appLeadSource', ['getAllAppLeadSource']),
    ...mapGetters('shortLeadInfo', ['getShortLead']),
    ...mapGetters('SuperAdminUsers', ['getAllStatesData']),
    ...mapGetters("InventoryCentral", ["getAllRegionsData"])
  },
  created() {
    this.appLoadData();
    this.fetchappData();
    this.trackChange();
  },
  methods: {
    ...mapActions('appDevice', ['FETCH_APP_DEVICES_DATA']),
    ...mapActions('Appvas', ['FETCH_VAS_DATAS']),
    ...mapActions('appLeadSource', ['FETCH_APP_LEADSOURCE_DATA']),
    ...mapActions('shortLead', ['STATE_SHORT_LEAD']),
    ...mapActions('shortLeadInfo', ['FETCH_SHORT_LEAD']),
    ...mapActions('SuperAdminUsers', ['FETCH_ALL_STATES_DATA', 'FETCH_PINCODE_WITH_TERM']),
    ...mapActions("InventoryCentral", ["FETCH_ALL_REGIONS_DATA"]),

    formatDate(val) {
      if (!val) return 'NA';
      const d = new Date(val);
      return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
    },

    trackChange() {
      this.formData.deviceCount = parseInt(this.formData.deviceCount) === 0 ? null : this.formData.deviceCount;
    },

    handleVasChange(newVal) {
      let updated = [...newVal];
      const has = val => updated.includes(val);
      const had = val => this.selectedVas.includes(val);
      if (had('EMI') && !has('EMI')) {
        updated = updated.filter(v => v !== 'Bank EMI' && v !== 'Brand EMI');
      }
      if (has('EMI') && !has('Bank EMI')) { updated.push('Bank EMI'); }
      if (has('Bank EMI') && !has('EMI')) { updated.push('EMI'); }
      if (has('Brand EMI') && !has('EMI')) { updated.push('EMI'); }
      this.selectedVas = [...new Set(updated)];
    },

    nameKeydown(e) {
      if (/^\W$/.test(e.key)) { e.preventDefault(); }
    },

    getDevice(val) {
      let self = this;
      self.FETCH_APP_DEVICES_DATA(val.id)
        .then(() => {
          self.dropDown.deviceOptions.splice(0);
          return _.map(this.getAllAppDevicesInfo, (item) => {
            self.dropDown.deviceOptions.push({ value: item, label: item.deviceName });
          });
        });
    },

    fnSubmitBankDetails(formData) {
      this.v$.formData.$touch();
      if (this.v$.formData.$error) {
        this.$q.notify('Please review fields again.');
      } else {
        if (this.formData.leadSource.multiTidEnabled == true) {
          this.formData.deviceCount = 1;
        }
        this.formData.vasInstanceMapping = JSON.stringify(this.selectedVas);
        this.formData.region = JSON.parse(formData.region);
        this.STATE_SHORT_LEAD(formData);
        this.shortlead = 'wiplead';
        this.fetchappData();
      }
    },

    devSelected() {
      this.$q.loading.show({ delay: 0, spinnerColor: 'purple-9', message: 'Fetching data ..' });
      let self = this;
      let deviceArr = [];
      this.FETCH_VAS_DATAS(this.formData.device.id).then((response) => {
        if (response.status == 200) {
          this.$q.loading.hide();
          self.getVasDeviceMapping.map(function(value) {
            deviceArr.push({ label: value.vas.name, value: value.vas.name });
          });
          this.selectBankEnableOptions = deviceArr;
          if (this.formData.device.deviceName == "Q161_PRO_DQR") {
            const upiOption = this.selectBankEnableOptions.find(opt => opt.label === "UPI QR");
            this.vasDisableFlag = true;
            if (upiOption) { this.selectedVas = [upiOption.value]; }
          } else {
            this.selectedVas = [];
            this.vasDisableFlag = false;
          }
          if (this.formData.device.deviceName == "Q161_PRO_SQR") {
            this.formData.deviceCount = 1;
            this.deviceFlag = true;
          } else {
            this.deviceFlag = false;
          }
        } else {
          this.$q.loading.hide();
          this.$q.notify({ color: 'negative', position: 'bottom-left', message: 'Invalid VAS!', icon: 'clear' });
          this.formData.device = '';
        }
      });
    },

    fnPincodeSearch(val, update) {
      if (val.length < 1) {
        update(() => { this.pincodeOptionsSearch = []; });
        return;
      }
      this.FETCH_PINCODE_WITH_TERM(val)
        .then(() => {
          update(() => {
            this.pincodeOptionsSearch = this.COMMON_FILTER_FUNCTION(this.getAllStatesData, val);
          });
        })
        .catch(() => { update(() => { this.pincodeOptionsSearch = []; }); });
    },

    pincodeSelected(item) {
      if (item) {
        this.pinSelected = true;
        this.formData.state = item.value.stateName;
        this.formData.city = item.value.cityName;
        this.formData.pincode = item.value.pincode;
        this.formData.pincodeTemp = item.value.pincode;
      }
    },

    fnClrPin() {
      if (!this.pinSelected) this.formData.pincodeTemp = '';
    },

    COMMON_FILTER_FUNCTION(arraySet, terms) {
      return _.filter(arraySet, function(oo) {
        return oo.label.toString().includes(terms.toLowerCase());
      });
    },

    fnShowEditShortLead(rowDetails) {
      this.propShowEditShortLead = !this.propShowEditShortLead;
      if (rowDetails != undefined) this.propRowDetails = rowDetails;
    },

    fnShowConvertToSat(rowDetails) {
      this.propShowConvertToSat = !this.propShowConvertToSat;
      if (rowDetails != undefined) this.propRowDetails = rowDetails;
    },

    appLoadData() {
      let self = this;
      self.FETCH_ALL_REGIONS_DATA().then(() => {
        return _.map(self.getAllRegionsData, (item) => {
          self.dropDown.regionOptions.push({ value: JSON.stringify(item), label: item.regionAreaName });
        });
      });
      self.FETCH_APP_LEADSOURCE_DATA().then(() => {
        if (JSON.parse(localStorage.getItem("u_i")).region.regionAreaName == 'VARANEEK') {
          return _.map(self.getAllAppLeadSource, (item) => {
            if (item.active && item.sourceName == 'VARANEEK')
              self.dropDown.leadSourceOptions.push({ value: item, label: item.sourceName });
          });
        } else {
          return _.map(self.getAllAppLeadSource, (item) => {
            if (item.active)
              self.dropDown.leadSourceOptions.push({ value: item, label: item.sourceName });
          });
        }
      });
    },

    fetchappData() { this.FETCH_SHORT_LEAD(); },

    goToSelectedTab(tab) {
      if (tab == "wiplead") {
        this.fetchappData();
      } else if (tab == "shortlead") {
        this.formData.leadName = '';
        this.formData.contactName = '';
        this.formData.contactNumber = '';
        this.formData.alternateContactNumber = '';
        this.formData.email = '';
        this.formData.deviceSelected = '';
        this.formData.leadAddress = '';
        this.formData.region = '';
        this.formData.pincode = '';
        this.formData.pincodeTemp = '';
        this.formData.state = '';
        this.formData.city = '';
        this.formData.leadSource = '';
        this.formData.device = '';
        this.formData.vasInstanceMapping = '';
        this.formData.deviceCount = '';
        this.formData.ownerFirstName = '';
        this.formData.ownerLastName = '';
        this.formData.ownerDOB = '';
        this.formData.data = '';
        this.selectedVas = [];
      }
    }
  }
};
</script>

<style>
.border-1 { border: 1px solid rgba(0, 0, 0, 0.1); }
.border-2 { border: 3px solid rgba(48, 48, 48, 0.5); }
</style>