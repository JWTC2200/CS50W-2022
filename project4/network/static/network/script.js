function myFunction(id) {
  alert(`${id} Hello from a static file!`);
  }

function likePost(id) {
  console.log("hello");
  
  fetch('/likepost',  {
    method: 'PUT',
    body: JSON.stringify({
      id: id,
    })
  })
  .then(response => response.json())
  .then(response => {
    console.log(response)
  } );

  
}