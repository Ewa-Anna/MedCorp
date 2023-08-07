<h1> MedCorp </h1>

This is a website for doctor's appointment registration for fictional medical company.
<b>Work still in progress.</b>
<br>
<h2> How to install and run the project? </h2>
<br>
1. Clone the repository
<br>
<code> git clone https://github.com/Ewa-Anna/MedCorp </code>
<br>
2. Install dependencies
<br>
<code> pip install -r requirements.txt </code>
<br>
3. Run the code
<br>
<code> flask --debug run </code>
<br>
<br>
<h2> Project overview </h2>
<p> This project contains three types of users: 
<ul>
<li> Patient - which is default, standard one, allowing user to book an existing appointment </li>
<li> Doctor - with accesses to create empty appointments slots </li>
<li> Admin - grants users accesses; create, edit and delete users; overview on applications content (like creating and maintaining specializations that can be assigned to doctors) </li>
</ul>
</p>
<p> All users can edit their profiles, maintain existing appointments (e.g. delete them) and use contact form. </p>