function myFunction() {
  user_name = document.querySelector("#user_name").innerHTML
  console.log(user_name);

  fetch('/following', {
    method: "PUT",
    body: JSON.stringify({
      to_follow: user_name,
    })
  })
  .then(response => response.json())
  console.log(response);
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