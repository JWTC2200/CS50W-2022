function myFunction() {
  follow_text = document.querySelector("#follow-button").innerHTML
  console.log(follow_text);
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
    const like_html = document.querySelector(`#${id}`)
    like_html.innerHTML = `❤ ${like_total}`
  } );

  
}