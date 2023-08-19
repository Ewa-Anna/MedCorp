<h1> MedCorp </h1>

This is a website for doctor's appointment registration for fictional medical company. Built with Flask framework and SQLAlchemy for database maintenance.
<br>
<h2> How to install and run the project? </h2>
<ol>
<li> Clone the repository</li>
<code> git clone https://github.com/Ewa-Anna/MedCorp </code>
<li> Install dependencies</li>
<code> pip install -r requirements.txt </code>
<li> Run the code
<ul>
<li>Debug version</li>
<code> flask --debug run </code>
<li> Production version</li>
<code> flask run </code>
</li>
</ul>
<li>Optional</li>
<p>For e-mail sending funtionality remember to follow .env.template with your Gmail EMAIL and PASSWORD generated for application uses.
<br> Follow support google article on how to generate password for application:
<a href="https://support.google.com/mail/answer/185833?hl=en"> https://support.google.com/mail/answer/185833?hl=en </a></p>
</ol>
<h2> Project overview </h2>
<p> This project contains three types of users: 
<ul>
<li> Patient - which is default, standard one, allowing user to book an existing appointment </li>
<li> Doctor - with accesses to create empty appointment slots </li>
<li> Admin - grants users accesses; create, edit and delete users; overview on applications content (like creating and maintaining specializations that can be assigned to doctors) </li>
</ul>
</p>
<p> All users can edit their profiles, maintain existing appointments (e.g. delete them) and use contact form. </p>