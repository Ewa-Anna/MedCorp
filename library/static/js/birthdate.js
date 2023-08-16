const maxDate = new Date();
const birthdate = new Date();
const today = new Date().toISOString().split('T')[0];
birthdate.setFullYear(maxDate.getFullYear() - 100); //allow user to setup birthdate max 100 years prior to today
const min_birthdate = birthdate.toISOString().split('T')[0];

document.getElementById("birthdate").setAttribute("min", min_birthdate);
document.getElementById("birthdate").setAttribute("max", today);
