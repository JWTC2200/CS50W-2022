function myFunction(id) {
  alert(`${id} Hello from a static file!`);
  }

function likePost(id) {
  const like_id = id.replace("like","")
  fetch('/likepost',  {
    method: 'PUT',
    body: JSON.stringify({
      id: like_id,
    })
  })
  .then(response => response.json())
  .then(response => {
    const like_total = response["count"]
    console.log(like_total);
    const like_html = document.querySelector(`#${id}`)
    console.log(like_html);
    like_html.innerHTML = `❤ ${like_total}`
  } );

  
}