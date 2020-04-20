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
  return v => v && v.length > 0 || customErrorMessage || `You must input a ${propertyType}`
}

/**
 * Validation function to establish the minimum length of a text input.
 * @param {*} propertyType type of the required field.
 * @param {*} minLength minimum lenght required.
 */
const minLength = (propertyType, minLength) => {
  return v => {
    if(!v){ return true; }

    return v.length >= minLength || `${propertyType} must be at least ${minLength} characters`;
  }
}

/**
 * Validation function to establish the maximum lenght of a text input.
 * @param {*} propertyType type of the required field.
 * @param {*} maxLength maximum lenght required.
 */
const maxLength = (propertyType, maxLength) => {
  return v => v && v.length <= maxLength || `${propertyType} must be less than ${maxLength} characters`
}


const maxSummaryLength = (propertyType, maxSummaryLength) => {
  return v => {
    if(!v){ return true; }
  
  return v.length <= maxSummaryLength || `${propertyType} must be less than ${maxSummaryLength} characters`
  }
}

/**
 * Validation fucntion that uses regex to establish the format for password within the syste.
 */
const nameFormat = () => {
  let regex = /^[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{1,}$/
  return v => regex.test(v) || "El formato del nombre es incorrecto,"
}

const passwordFormat = () => {
  let regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{10,64}$/
  return v => regex.test(v) || "Password must contain at least: 1 upercase, 1 lowercase, 1 number, and 1 special character."
}

/**
 * Validation fucntion that uses regex to establish email format
 */
const emailFormat = () => {
  let regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return v => regex.test(v) || "Not a valid email format."
}

/**
 * Validation fucntion to determine if password field and comfirm field match.
 * @param {*} password pasword to match to.
 */
const passwordMatch = (password) => {
  return v => v === password || "Password does not match."

}

const generalPhrase = (propertyType) =>{
    
    let regex = /^[a-zA-Z0-9- ',.;:!]*$/
    return v => regex.test(v) || `El formato de ${propertyType} es incorrecto.`
  
}
const alphaSpaces = (propertyType) =>{
  let regex = /^[a-zA-Z ]*$/
  return v => regex.test(v) || `El formato de ${propertyType} es incorrecto.`
}

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
  return v => v !== password || "Password password can't be the same as the previous one."

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
  passwordDiffFromOld

}