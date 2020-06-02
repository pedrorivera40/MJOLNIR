<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="display-1">{{page_title}}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <p style="word-break: normal;">{{page_description}}</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="(member, idx) in members" :key="idx">
        <ProfileCard
          :name="member.name"
          :img="member.img"
          :major="member.major"
          :position="member.position"
        />
      </v-col>
    </v-row>
    <v-spacer></v-spacer>
    <v-row>
      <v-col align="center">
        <h1 class="my-4 display-1">Síguenos en nuestras redes sociales</h1>
      </v-col>
    </v-row>
    <v-row class="my-4">
      <v-col align="center">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn color="#3b5998" fab x-large dark href="ENTER_URL" target="_blank" v-on="on">
              <v-icon>mdi-facebook</v-icon>
            </v-btn>
          </template>
          <span>Síguenos en Facebook</span>
        </v-tooltip>
      </v-col>
      <v-col align="center">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn color="#00acee" fab x-large dark href="ENTER_URL" target="_blank" v-on="on">
              <v-icon>mdi-twitter</v-icon>
            </v-btn>
          </template>
          <span>Síguenos en Twitter</span>
        </v-tooltip>
      </v-col>
      <v-col align="center">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn color="#C13584" fab x-large dark href="ENTER_URL" target="_blank" v-on="on">
              <v-icon>mdi-instagram</v-icon>
            </v-btn>
          </template>
          <span>Síguenos en Instagram</span>
        </v-tooltip>
      </v-col>
      <v-col align="center">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn color="#2867B2" fab x-large dark href="ENTER_URL" target="_blank" v-on="on">
              <v-icon>mdi-linkedin</v-icon>
            </v-btn>
          </template>
          <span>Síguenos en LinkedIn</span>
        </v-tooltip>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProfileCard from "../components/ProfileCard";
export default {
  components: {
    ProfileCard
  },
  data() {
    return {
      page_title: "Sobre Nosotros",
      page_description:
        "Ante la falta de un medio que informase el desempeño deportivo de las juanas y tarzanes durante la liga atlética interuniversitaria (LAI), Huella Deportiva es fundado por un grupo de estudiantes colegiales en el año 2015. Huella Deportiva cuenta con experiencia trabajando magnos eventos deportivos como las justas. Esta organización presenta herramientas y escenarios en donde los universitarios se pueden desarrollar en el área de la narración, fotografía, edición de videos, escritura deportiva, producción, diseño gráfico, entretenimiento deportivo, desarrollo de páginas web, entre otras áreas. Por tal motivo, Huella Deportiva no solo tiene como misión el ofrecer cobertura mediática al deporte colegial, sino que también desea proveer un medio a los estudiantes colegiales donde puedan entrar en contacto con en el mundo de las comunicaciones. De igual forma, tenemos como visión el poder desarrollar profesionales visionarios, creativos y con liderazgo para el desarrollo social, cultural y económico tanto de Puerto Rico, como del resto del mundo.",
      members: [
        {
          name: "Melvin Soto",
          img:
            "https://lh3.googleusercontent.com/pw/ACtC-3cgh9L7H4R5RYAooVGOy5yt49cJce4CQMkIukfbTOIlcbkflJTzzZ5lwGzP17O01nPHVMVwkH6qpiTSVzDnnH8CEbeAlKrPfEYOIeLB_Npd876f5WGDIo0X4OngjLWxpiVDxsEdqknOjrijHYdBx-B9=s648-no?authuser=0",
          position: "Director de Operaciones",
          major: "Sistemas Computarizados de Información"
        },
        {
          name: "Edmarie Santana",
          img:
            "https://lh3.googleusercontent.com/pw/ACtC-3dIDGhNHyol3uTmY6c30XEhzW4cHshCdWaept86s1F11DTYr4i0H4hIHGQt-VFi3iqyzmWzeKCFkUCRc0P-Y_Kas0kpkRafAGraRx_sOjWdkJ58ygRGXSaH9DqGDJzTFm1ZFDziAbNn0D2_W4gfzjn9=s648-no?authuser=0",
          position: "Departamento de Información y Estadísticas",
          major: "Ingeniería de Computadoras"
        },
        {
          name: "Roberto Rodríguez",
          img:
            "https://lh3.googleusercontent.com/pw/ACtC-3cyiCI77j4Bhbf6tbBykt1ge5LhuZPOqu_zzi4guen6XQgDqWNvgGm3-wc31JLC0a1MEsvCDa7gBAb8y0u5XFxY-i15biULGlLEivYGq6Y3XnNJ_Jq3Qtv2af8EyBkcYlbgfNMpTdHue1JgOGxiWuwg=s648-no?authuser=0",
          position: "Departamento de Producción",
          major: "Ingeniería Civil"
        },
        {
          name: "Emilio Pérez",
          img:
            "https://lh3.googleusercontent.com/pw/ACtC-3d5bC5DAz8-8hWoFnNMEgksW-jbFOr7oHM8uVmzXOatHgjj49vq4JAlV2hCXtrI0ceUODRqH0o11JDPTKLakDDiKwnCVrIJ6YYD0bxnAHzPzkhLMf2aog66IilPUHdUjNFBo6e9keKt04OIUDq4Rrsp=s648-no?authuser=0",
          position: "Departamento de Producción",
          major: "Ingeniería Industrial"
        },
        {
          name: "Milton Rodríguez",
          img:
            "https://lh3.googleusercontent.com/pw/ACtC-3flh2BvRiknsQXkrtbRxIdTrPVMyH_0qfBjs0qaBsPKuLpw4lzKhZS_8uAo0hUn8JBplav7tk_UUaZiXl8h7v-zXeoHvn_CfGMO0WpK92lplxOPms1HsIDfCONUvzGOiV5IrtIcPhkqmA0Twdf8Hn74=s648-no?authuser=0",
          position: "Departamento de Contenido Creativo / Diseño Gráfico",
          major: "Ingeniería Civil"
        },
        {
          name: "Luis Díaz",
          img:
            "https://lh3.googleusercontent.com/pw/ACtC-3djWCcSG1goO8baNO_P-ztWpx3aaoENMsFz7rURw932i5SOcPZ8mYxPOS4RqjeWc8AlVvVPdzoVvW_klEd9F6Y2Tysa4g5rHK8PjvxFdI9NC-3_6IrJMIKnxJBQ4YJrvvhfm5lxHfgzMt1ISewTMguf=s648-no?authuser=0",
          position: "Departamento de Comunicación Deportiva",
          major: "Biología y Literatura Comparada"
        },
        {
          name: "Coralis Rodríguez",
          img:
            "https://lh3.googleusercontent.com/pw/ACtC-3ffi5qGzBIIVyiLJ-yfHaWzXnWWkmdJXXoeWNtfgmYk-t-xQzWkAE-xG3TqbXJNDixCGnSKqOXFSjH99PVa_IKMdmEGBd9JoRE56GS5qutYtJm9B5mu6QH7E4xky2UBQ8OV8fJt2oRmKbQLPtK3eWaQ=s648-no?authuser=0",
          position: "Departamento de Contenido Creativo / Fotógrafa",
          major: "Manejo de Proyectos"
        }
      ]
    };
  }
};
</script>