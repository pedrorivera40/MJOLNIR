<template>
<!-- TODO: Verify how to pass the team ID, if by route or some other way -->
<!-- TODO: Check/Confirm that query exists in order to get all athletes of one sport, at least the name fields + ID -->
<!-- TODO: Check how to make field dynamic in order to add multiple, and be able to remove some from addlist before adding/submitting. -->
<!-- TODO: instead of a list of all athletes in sport, it could be a search...no idea how to do that though. -->
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
        <v-toolbar-title>Añadir Atleta a Equipo {{sport}} - {{branch}}</v-toolbar-title>
        <v-spacer />
    </v-toolbar>
    <v-card-text>            
      <ValidationObserver ref="observer" v-slot="{ validate, reset }">
        <form>
            <v-container>  
                <v-row>
                    <v-col>
                        <v-row>
                            <template v-slot:progress>
                            <v-progress-linear
                                absolute
                                color="green lighten-3"
                                height="4"
                                indeterminate
                            ></v-progress-linear>
                            </template>
                            
                            <v-form>
                            </v-form>
                            <v-divider></v-divider>
                        </v-row>
                        <v-row>      
                            <div>                  
                            <h2>
                                Atleta:
                            </h2>
                            </div> 
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col                   
                            >
                               <v-autocomplete
                                    v-model="members_to_add"
                                    :items="sport_athletes"
                                    filled
                                    chips
                                    color="blue-grey lighten-2"
                                    label="Select"
                                    item-text="athlete_name"
                                    item-value="athlete_id"
                                    multiple
                                    >
                                    <template v-slot:selection="data">
                                        <v-chip
                                        v-bind="data.attrs"
                                        :input-value="data.selected"
                                        close
                                        @click="data.select"
                                        @click:close="remove_from_select(data.item)"
                                        >
                                        <v-avatar left>
                                            <v-img :src="data.item.profile_image_url"></v-img>
                                        </v-avatar>
                                        {{ data.item.athlete_name }}
                                        </v-chip>
                                    </template>
                                    <template v-slot:item="data">
                                        <template v-if="typeof data.item !== 'object'">
                                        <v-list-item-content v-text="data.item"></v-list-item-content>
                                        </template>
                                        <template v-else>
                                        <v-list-item-avatar>
                                            <img :src="data.item.profile_image_url">
                                        </v-list-item-avatar>
                                        <v-list-item-content>
                                            <v-list-item-title v-html="data.item.athlete_name"></v-list-item-title>
                                        </v-list-item-content>
                                        </template>
                                    </template>
                                    </v-autocomplete>
                            </v-col>
                        </v-row>    
                    </v-col>  
                </v-row>      
                <v-row justify="end">
                        <v-btn class="mr-4" @click="submit">submit</v-btn>
                </v-row>   
            </v-container>
        </form>
      </ValidationObserver>
    </v-card-text>
  </v-card>
</template>

<script>
    import { required, email, max, alpha_spaces, alpha, alpha_dash, regex,required_if } from 'vee-validate/dist/rules'
    import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'

  setInteractionMode('eager')

  extend('required', {
    ...required,
    message: '{_field_} no puede estar vacio',
  })

  extend('max', {
    ...max,
    message: '{_field_} no puede contener mas de {length} caracteres',
  })

  extend('email', {
    ...email,
    message: 'Email must be valid',
  })

  extend('alpha',{
    ...alpha,
    message: "{_field_} solamente debe tener caracteres",
  })

  extend('alpha_spaces',{
    ...alpha_spaces,
    message: "{_field_} solamente debe contener caracters,guiones y/o espacios",
  })
  extend('alpha_dash',{
    ...alpha_dash,
    message: "{_field_} puede contener un guiones",
  })
  extend('regex',{
    ...regex,
    message:"El campos es invalido",
  })
  extend('required_if',{
    ...required_if,
    message:"La posicion es requerida para este deporte",
  })
  

  export default {
    components: {
        ValidationProvider,
        ValidationObserver,
    },
    data: () => ({
        sport_id:1,
        team_id:1,
        // TODO: (Herbert) Verificar como hacer que esto [sport and branch] sea dinamico, pasado por el sport previo
        sport:'Baloncesto',  
        branch:'Masculino',    
        sport_athletes:[
            {
                athlete_name: "Bruce Wayne",
                athlete_id: "1",
                profile_image_url: "https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/18056978_1321492691261909_7453541174330533269_n.jpg?_nc_cat=102&_nc_sid=8024bb&_nc_oc=AQmWfwxDy-LTXcZv4K0hcL8VNdr4F0JDlBW90Hq3YG157GtEuXYnB-AKL6hNki0uuh4&_nc_ht=scontent-mia3-2.xx&oh=6dc80a0cb41e6c693897b317148b3753&oe=5EB4AFCF"
            },
            {
                athlete_name: "Richard Grayson",
                athlete_id: "2",
                profile_image_url: "https://vignette.wikia.nocookie.net/marvel_dc/images/a/a2/Nightwing_0008.jpg/revision/latest?cb=20111009075845"
                
            },
            {
                athlete_name: "Clark Kent",
                athlete_id: "3",
                profile_image_url:"https://pbs.twimg.com/media/DUOPKlWU0AEGY0S.jpg:large"
            },
            {
                athlete_name: "Hal Jordan",
                athlete_id: "4",
                profile_image_url:"https://pbs.twimg.com/profile_images/671792891333705728/cbj6SLRA_400x400.jpg"
            },
            {
                athlete_name: "John Stewart",
                athlete_id: "5",
                profile_image_url:"https://pbs.twimg.com/profile_images/378800000008348088/c27e2c3cfc006292e4782888419c9a5b.jpeg"
            },
            {
                athlete_name: "Wallace West",
                athlete_id: "6",
                profile_image_url:"https://pbs.twimg.com/profile_images/702836497679040512/VGriLvTv_400x400.jpg"
            },
            {
                athlete_name: "Arthur Curry",
                athlete_id: "7",
                profile_image_url:"https://pbs.twimg.com/profile_images/720648822242852864/4tkk3y8S_400x400.jpg"
            },
            {
                athlete_name: "Jason Todd",
                athlete_id: "8",
                profile_image_url:"https://pbs.twimg.com/profile_images/378800000191599213/de16556e163c156aad36be8520235133.png"
            },
            {
                athlete_name: "Timothy Drake",
                athlete_id: "9",
                profile_image_url:"https://pbs.twimg.com/profile_images/3478040423/a3b79463a31c644dda362f1f4bc845b9.jpeg"
            },
            {
                athlete_name: "Victor Stone",
                athlete_id: "10",
                profile_image_url:"https://www.dccomics.com/sites/default/files/imce/2018/08-AUG/Cyborg_v01_r01_5b6c7d7bef1616.90753062.jpg"
            },
            {
                athlete_name: "John Constantine",
                athlete_id: "11",
                profile_image_url:"https://pbs.twimg.com/profile_images/669770942164238336/pXR6Znwe_400x400.jpg"
            },
            {
                athlete_name: "Simon Baz",
                athlete_id: "12",
                profile_image_url:"https://pbs.twimg.com/profile_images/1030138980011069440/g3ckdN2u_400x400.jpg"
            }
        ],
        members_to_add:[],
        yearList:[],
    }),
           
    methods: {
        remove_from_select (item) {
            const index = this.members_to_add.indexOf(item.athlete_id)
            if (index >= 0) this.members_to_add.splice(index, 1)
        },
    
        submit () {
            this.$refs.observer.validate()
            console.log("Going to add athletes to team with id "+this.team_id+".")
            console.info(this.members_to_add)
            this.goToTeam()
        },

        getSport(){
            return this.sport
        },
        goToTeam(){
             this.$router.push('/equipo/')
        }
    },
  }
    // The Only Arguments we need. 
    //{
    //"sport_id":1,   -->selected from existing
    //"season_year":"2020", --> selected from yearList
    //"team_image_url":"www.google.com" -->inserted, optional
    //"about_team": "some text" --> inserted, optional
    //}
</script>