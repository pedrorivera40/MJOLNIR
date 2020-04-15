const required = (propertyType, customErrorMessage) => { 
  return v => v && v.length > 0 || customErrorMessage || `You must input a ${propertyType}`
}
const minLength = (propertyType, minLength) => {
  return v => {
    if(!v){ return true; }

    return v.length >= minLength || `${propertyType} must be at least ${minLength} characters`;
  }
}
const maxLength = (propertyType, maxLength) => {
  return v => v && v.length <= maxLength || `${propertyType} must be less than ${maxLength} characters`
}

const maxSummaryLength = (propertyType, maxSummaryLength) => {
  return v => {
    if(!v){ return true; }
  
  return v.length <= maxSummaryLength || `${propertyType} must be less than ${maxSummaryLength} characters`
  }
}

const passwordFormat = () => {
  let regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{10,64}$/
  return v => regex.test(v) || "Password must contain at least: 1 upercase, 1 lowercase, 1 number, and 1 special character."
}
const emailFormat = () => {
  let regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return v => regex.test(v) || "Not a valid email format."
}

const passwordMatch = (password) => {
  return v => v === password || "Password does not match."

}

const teamRequired = (propertyType) => {
  return v => {
    if(!v){ return `${propertyType} debes ser seleccionado`; }
    
    //Will receive the id of the team which will be an integer larger than zero.
    return v >= 0 || `${propertyType} debes ser seleccionado`;
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
}