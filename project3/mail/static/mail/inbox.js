document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(reply_data) {
  console.log(reply_data);

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-table').style.display = 'none';
  document.querySelector('#email-single').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  if (reply_data.sender != undefined) {
    document.querySelector('#compose-recipients').value = reply_data.sender;
    document.querySelector('#compose-subject').value = `Re: ${reply_data.subject}`;
    document.querySelector('#compose-body').value = `On ${reply_data.timestamp} ${reply_data.sender} wrote: ${reply_data.body}`;
  }

  document.querySelector('#compose-form').addEventListener("submit", function(evt){
    evt.preventDefault();
  }, true);

  document.querySelector('#submit').addEventListener('click', send_email)
}

function send_email() {
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector("#compose-body").value;

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
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-table').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-single').style.display = 'none';

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
    if (mailbox === 'archive') {
      load_archivebox(emails)
    }
});
}

function load_inbox(emails) {
  // load headings
  const email_table = document.querySelector('#email-table');
  if (emails.length === 0) {
    email_table.innerHTML = "You have no emails in your inbox folder"
  }
  else {
    email_table.innerHTML = 
  `<div class="row">
    <div class="col">Sender</div>
    <div class="col">Subject</div>
    <div class="col">Date Recieved</div>     
  </div>`;
  emails.forEach(function (email) {
    //add s
    const email_list = document.createElement('a');
    if (email.read === false) {
       email_list.innerHTML= 
        `<div class="row bg-light border border-dark link-secondary">
          <div class="col">${email.sender}</div>
          <div class="col">${email.subject}</div>
          <div class="col">${email.timestamp}</div>
        </div>`;
    }
    else {
      email_list.innerHTML=
      `<div class="row text-white bg-secondary border border-dark link-light">
          <div class="col">${email.sender}</div>
          <div class="col">${email.subject}</div>
          <div class="col">${email.timestamp}</div>
        </div>`;

    }
    email_table.append(email_list);
    email_list.addEventListener('click', () => open_email(email.id, 'inbox'));
  });
  }
}

function open_email(email_id, route) {
  const inbox_buttons = document.querySelector('#inbox-buttons');
  const reply_button = document.querySelector('#reply-button');
  const archive_button = document.querySelector('#archive-button');
  const archive_buttons = document.querySelector('#archive-buttons');
  const unarchive_button = document.querySelector('#unarchive-button');

  inbox_buttons.style.display = 'none';
  archive_buttons.style.display = 'none';

  // set email to read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  //get the email from id
  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#email-table').style.display = 'none';
    document.querySelector('#email-single').style.display = 'block';

    document.querySelector('#eview-sender').innerHTML = `From: ${email.sender}`;
    document.querySelector('#eview-to').innerHTML = `To: ${email.recipients}`;
    document.querySelector('#eview-subject').innerHTML = `Subject: ${email.subject}`;
    document.querySelector('#eview-timestamp').innerHTML = `Timestamp: ${email.timestamp}`;
    document.querySelector('#eview-body').innerHTML = `${email.body}`;
    
    if (route === 'inbox') {
      inbox_buttons.style.display = 'block';
    };
    if (route === 'archive') {
      archive_buttons.style.display = 'block';
    }
    reply_button.addEventListener('click', () => compose_email(email));
    archive_button.addEventListener('click', () => archiveEmail(email_id, true));
    unarchive_button.addEventListener('click', () => archiveEmail(email_id, false));
    
  });
}

function load_sentbox(emails) {
  const email_table = document.querySelector('#email-table');
  if (emails.length === 0) {
    email_table.innerHTML = "You have no emails in your sent folder"
  }
  else {
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
  
}

function archiveEmail(email_id, command) {
  // update archive status
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify ({
      archived: command
    })
  })
  load_mailbox('inbox');
}

function load_archivebox(emails) {
  const email_table = document.querySelector('#email-table');
  console.log(emails);
  if (emails.length === 0) {
    email_table.innerHTML = "You have no emails in your archive folder"
  }
  else {
    email_table.innerHTML = 
      `<div class="row">
        <div class="col">Sender</div>
        <div class="col">Subject</div>
        <div class="col">Date Recieved</div>     
      </div>`;
    emails.forEach(function (email) {
      //add table
      const email_list = document.createElement('a');
      email_list.innerHTML= 
        `<div class="row bg-light border border-light">
          <div class="col">${email.sender}</div>
          <div class="col">${email.subject}</div>
          <div class="col">${email.timestamp}</div>
        </div>`;
      email_table.append(email_list);
      email_list.addEventListener('click', () => open_email(email.id, 'archive'));
    });
  }  
}