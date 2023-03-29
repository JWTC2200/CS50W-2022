document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#test').addEventListener('click', () => {
    console.log(document.querySelector('#compose-body').value);
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').addEventListener("submit", function(evt){
    evt.preventDefault();
  }, true);

  // fetch
  document.querySelector('input[type="submit"]').addEventListener('click', () => {

    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector("#compose-body").value;

    console.log(subject);
  
    fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: `${recipients}`,
        subject: `${subject}`,
        body: `${body}`
        })
    })
    .then(response => response.json())
    .then(()=>load_mailbox('sent'));
  });


}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  const email_table = document.querySelector('#email-table');
  email_table.innerHTML = "";
    
  fetch(`emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
    // Inbox
    if (mailbox === 'inbox') {
      load_inbox(emails)
    }
    if (mailbox === 'sent') {
      load_sentbox(emails)
    }
});
}

function load_inbox(emails) {
  // load headings
  const email_table = document.querySelector('#email-table');
  email_table.innerHTML = 
  `<div class="row">
    <div class="col">Sender</div>
    <div class="col">Subject</div>
    <div class="col">Date Recieved</div>     
  </div>`;
  emails.forEach(function (email) {
    //add table
    const email_list = document.createElement('a');
    if (email.read === false) {
       email_list.innerHTML= 
        `<div class="row bg-light border border-light">
          <div class="col">${email.sender}</div>
          <div class="col">${email.subject}</div>
          <div class="col">${email.timestamp}</div>
        </div>`;
    }
    else {
      `<div class="row bg-secondary border border-dark">
          <div class="col">${email.sender}</div>
          <div class="col">${email.subject}</div>
          <div class="col">${email.timestamp}</div>
        </div>`;
    }
    email_table.append(email_list);
    email_list.addEventListener('click', () => open_email(email.id));
  });
}

function open_email(email_id) {
  //get the email from id
  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email)
  });
}

function load_sentbox(emails) {
  const email_table = document.querySelector('#email-table');
  email_table.innerHTML = 
  `<div class="row">
    <div class="col">Recipient</div>
    <div class="col">Subject</div>
    <div class="col">Date Sent</div>     
  </div>`;
  emails.forEach(function (email) {
    const email_list = document.createElement('a');
    email_list.innerHTML= 
      `<div class="row bg-light border border-light">
        <div class="col">${email.recipients}</div>
        <div class="col">${email.subject}</div>
        <div class="col">${email.timestamp}</div>
      </div>`;
    email_table.append(email_list);
    email_list.addEventListener('click', () => open_email(email.id));
  })
}