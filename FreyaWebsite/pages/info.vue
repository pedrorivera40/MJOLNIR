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
            "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdYitBSd21DwpX2l0twNN-u5wHL0NcO9iJSQv2uhe7Qf3yQKJ5&usqp=CAU",
          position: "Director de Operaciones",
          major: "Sistemas Computarizados de Información"
        },
        {
          name: "Emilio Pérez",
          img:
            "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdYitBSd21DwpX2l0twNN-u5wHL0NcO9iJSQv2uhe7Qf3yQKJ5&usqp=CAU",
          position: "Departamento de Producción",
          major: "Ingeniería Industrial"
        },
        {
          name: "Milton Rodríguez",
          img:
            "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdYitBSd21DwpX2l0twNN-u5wHL0NcO9iJSQv2uhe7Qf3yQKJ5&usqp=CAU",
          position: "Departamento de Contenido Creativo / Diseño Gráfico",
          major: "Ingeniería Civil"
        },
        {
          name: "Coralis Rodríguez",
          img:
            "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdYitBSd21DwpX2l0twNN-u5wHL0NcO9iJSQv2uhe7Qf3yQKJ5&usqp=CAU",
          position: "Departamento de Contenido Creativo / Fotógrafa",
          major: "Manejo de Proyectos"
        },
        {
          name: "Luis Díaz",
          img:
            "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdYitBSd21DwpX2l0twNN-u5wHL0NcO9iJSQv2uhe7Qf3yQKJ5&usqp=CAU",
          position: "Departamento de Comunicación Deportiva",
          major: "Biología y Literatura Comparada"
        },
        {
          name: "Edmarie Santana",
          img:
            "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdYitBSd21DwpX2l0twNN-u5wHL0NcO9iJSQv2uhe7Qf3yQKJ5&usqp=CAU",
          position: "Departamento de Información y Estadísticas",
          major: "Ingeniería de Computadoras"
        }
      ]
    };
  }
};
</script>