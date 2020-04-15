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

export default {
  required,
  minLength,
  maxLength,
  passwordFormat,
  passwordMatch,
  emailFormat
}