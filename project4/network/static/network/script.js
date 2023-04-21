function followUser() {
  user_name = document.querySelector("#user_name").innerHTML
  console.log("test");

  fetch('/following', {
    method: "PUT",
    body: JSON.stringify({
      to_follow: user_name,
    })
  })
  .then(response => response.json())
  .then(response => {
    const follow_txt = response["follow_status"]
    const follower_count = response["follow_count"]
    console.log(follow_txt)
    const follow_button = document.querySelector("#follow-button")
    const follow_count = document.querySelector("#follow-count")
    follow_count.innerHTML = `Followers: ${follower_count}`
    follow_button.innerHTML = follow_txt
    console.log(follow_button)
  });
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