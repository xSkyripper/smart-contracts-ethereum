<template>
  <div class="container contracts">
    <h1>{{ msg }}</h1>
    <div class="row">
      <ContractComponent
        v-for="r in resources"
        :key="r.id"
        :name="r.name"
        :picture="r.picture"
        :due_date="r.due_date"
        :service="r.service"
        :location="r.location"
        :admin=$route.meta.admin
      />
    </div>
  </div>
</template>

<script>
import ContractComponent from '@/components/ContractComponent.vue'

export default {
  name: 'ContractsComponent',
  components: {
    ContractComponent
  },
  props: {
    msg: String
  },
  data () {
    return {
      resources: [
        {
          id: 0,
          name: 'E-On',
          picture: require('../assets/e_on.jpg'),
          due_date: '2018-12-03',
          service: 'Electric Energy',
          location: 'Iasi, Iasi'
        },
        {
          id: 1,
          name: 'E-On',
          picture: require('../assets/e_on.jpg'),
          due_date: '2018-11-29',
          service: 'Gas',
          location: 'Iasi, Iasi'
        },
        {
          id: 2,
          name: 'ANAF',
          picture: require('../assets/anaf.jpg'),
          due_date: '2018-12-05',
          service: 'Car Tax',
          location: 'Iasi, Iasi'
        },
        {
          id: 3,
          name: 'City Hall',
          picture: require('../assets/iasi.jpg'),
          due_date: '2018-12-01',
          service: 'Garbage Tax',
          location: 'Iasi, Iasi'
        },
        {
          id: 4,
          name: 'E-On',
          picture: require('../assets/e_on.jpg'),
          due_date: '2018-11-29',
          service: 'Gas',
          location: 'Iasi, Iasi'
        },
        {
          id: 5,
          name: 'ANAF',
          picture: require('../assets/anaf.jpg'),
          due_date: '2018-12-05',
          service: 'Car Tax',
          location: 'Iasi, Iasi'
        },
        {
          id: 6,
          name: 'City Hall',
          picture: require('../assets/iasi.jpg'),
          due_date: '2018-12-01',
          service: 'Garbage Tax',
          location: 'Iasi, Iasi'
        }
      ],
      error: ''
    }
  },
  methods: {
    contracts () {
      alert('Contracts')
    }
  }
}
</script>

<style lang="scss" scoped>
.contracts {
  h1 {
    margin-bottom:30px;
  }

  margin-top:30px;
}
</style>
