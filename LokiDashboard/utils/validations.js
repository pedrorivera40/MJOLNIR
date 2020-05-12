/**
 * Module to specify rules to validate text inputs.
 * @module validations
 */


/**
 * Validation function to denote a required field.
 * @param {*} propertyType type of the required field.
 * @param {*} customErrorMessage Custom error message fro when the rule is not met.
 */
const required = (propertyType, customErrorMessage) => { 
  return v => v && v.length > 0 || customErrorMessage || `Favor de ingresar ${propertyType}`
}

/**
 * Validation function to establish the minimum length of a text input.
 * @param {*} propertyType type of the required field.
 * @param {*} minLength minimum lenght required.
 */
const minLength = (propertyType, minLength) => {
  return v => {
    if(!v){ return true; }

    return v.length >= minLength || `${propertyType} debe ser mayor de ${minLength} caracteres`;
  }
}

/**
 * Validation function to establish the maximum lenght of a text input.
 * @param {*} propertyType type of the required field.
 * @param {*} maxLength maximum lenght required.
 */
const maxLength = (propertyType, maxLength) => {
  return v => v && v.length <= maxLength || `${propertyType} debe ser menor de ${maxLength} caracteres`
}

/**
 * Validation function to establish the maximum length of a summary text input.
 * @param {*} propertyType type of the required field.
 * @param {*} maxSummaryLength maximum length of the summary
 */
const maxSummaryLength = (propertyType, maxSummaryLength) => {
  return v => {
    if(!v){ return true; }
  
  return v.length <= maxSummaryLength || `${propertyType} must be less than ${maxSummaryLength} characters`
  }
}

/**
 * Valitation function that uses regex to establish the format for  a name given as input.
 */
const nameFormat = () => {
  let regex = /^[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{0,}$/
  return v => regex.test(v) || "El formato del nombre es incorrecto,"
}

/**
 * Validation function that uses regex to establish the format for password within the syste.
 */
const passwordFormat = () => {
  let regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{10,64}$/
  return v => regex.test(v) || "La contraseña debe contener al menos: 1 mayúscula, 1 minúscula, 1 número y 1 caracter especial."
}

/**
 * Validation fucntion that uses regex to establish email format
 */
const emailFormat = () => {
  let regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return v => regex.test(v) || "No es un formato valido de correo electrónico."
}

/**
 * Validation fucntion to determine if password field and comfirm field match.
 * @param {*} password pasword to match to.
 */
const passwordMatch = (password) => {
  return v => v === password || "Las contraseñas no coinciden."

}

/**
 * Validation function that uses regex to establish the format for a general phrase given as input.
 */
const generalPhrase = (propertyType) =>{
    
    let regex = /^[a-zA-Z0-9- ',.;:!]*$/
    return v => regex.test(v) || `El formato de ${propertyType} es incorrecto.`
  
}

/**
 * Validation function to check if only using numeric values
 * @param {*} propertyType type of the required field
 */
const numeric = (propertyType) =>{
  let regex = /^[0-9]*$/
  return v => regex.test(v) || `El formato de ${propertyType} es incorrecto.`

}

/**
 * Validation function that uses regex to verify that the input given only has alpha or space characters.
 * @param {*} propertyType type of the required field
 */
const alphaSpaces = (propertyType) =>{
  let regex = /^[a-zA-Z ]*$/
  return v => regex.test(v) || `El formato de ${propertyType} es incorrecto.`
}

/**
 * Validation function that verifies whether a team has been given as input.
 * @param {*} propertyType type of the required field
 */
const teamRequired = (propertyType) => {
  return v => {
    if(!v){ return `${propertyType} debes ser seleccionado`; }
    
    //Will receive the id of the team which will be an integer larger than zero.
    return v >= 0 || `${propertyType} debes ser seleccionado`;
  }
}

/**
 * Validation function to determine if temp password and new password are different.
 * @param {*} password password to differentiate from.
 */
const passwordDiffFromOld = (password) => {
  return v => v !== password || "La nueva contraseña no puede ser igual a la contraseña anterior."

}

/**
 * Validation function to determine a season was chosen properly
 * @param {*} propertyType  type of the required field
 */
const seasonRequired = (propertyType) => {
  return v => {
    if(!v){ return `${propertyType} debe ser seleccionado`; }
    
    //Will receive the year of the season which will be an integer larger or equal than 2020.
    return v >= 2020 || `${propertyType} debe ser seleccionado`;
  }
}

/**
 * Validation function to determine a number input properly
 * @param {*} propertyType  type of the required field
 */
const scoreRequired = (propertyType) => {
  return v => {
    if((!v)&&(v!=0)){ return `${propertyType} es un campo requerido`; }
    
    //Will receive the score of the team which will be an integer larger or equal than zero.
    return v >= 0 || `${propertyType} es un campo requerido`;
  }
}

export default {
  required,
  minLength,
  maxLength,
  maxSummaryLength,
  passwordFormat,
  passwordMatch,
  emailFormat,
  teamRequired,
  nameFormat,
  generalPhrase,
  alphaSpaces,
  passwordDiffFromOld,
  seasonRequired,
  numeric,
  scoreRequired

}