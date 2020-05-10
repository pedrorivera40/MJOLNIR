import firebase from 'firebase'
import firebaseConfig from './firebaseConfig'


/* Check if there is one firebase app already initialized, if not, intialize it. 
Otherwise, use the curret app. This avoids errors with 'duplicate' firebase apps. */
export function rtdb() {
    return !firebase.apps.length ? firebase.initializeApp(firebaseConfig).database() : firebase.app().database()
}