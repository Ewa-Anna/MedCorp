//min date to choose in calendar should be today
const today = new Date().toISOString().split('T')[0]; //strip Date() from time; format: YYYY-MM-DD
const maxDate = new Date();
maxDate.setFullYear(maxDate.getFullYear() + 1); //max date to choose in calendar should be today + 1 year
const max_date = maxDate.toISOString().split('T')[0];

document.getElementById("selected_date").setAttribute("min", today);
document.getElementById("selected_date").setAttribute("max", max_date);
