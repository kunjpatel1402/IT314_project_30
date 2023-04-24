let user = '<%- JSON.stringify(user) %>';
user = JSON.parse(user);

function color(status, id1) {
  let upbutton = document.getElementById("up/" + id1);
  let downbutton = document.getElementById("down/" + id1);
  if (status === "upvoted") {
    upbutton.style.color = "lime";
    downbutton.style.color = "black";
  }
  else if (status === "downvoted") {
    downbutton.style.color = "red";
    upbutton.style.color = "black";
  }
  else {
    downbutton.style.color = "black";
    upbutton.style.color = "black";
  }
}

function add_verified(votes) {
  let verified0 = document.getElementById("verified0");
  let verified1 = document.getElementById("verified1");
  if (votes >= 100) {
    if (verified0) {
      verified0.innerHTML = "";
      verified0.style.marginLeft = "0px";
    }
    verified1.style.marginLeft = "1%";
    verified1.innerHTML = "&#x2713;";
  }
  else {
    if (verified0) {
      verified0.innerHTML = "";
      verified0.style.marginLeft = "0px";
    }
    if (verified1) {
      verified1.innerHTML = "";
      verified1.style.marginLeft = "0px";
    }
  }

}

let verified = document.getElementById("verified");
function upclick(id) {
  const id1 = id.split("/")[1];
  console.log("clicked");
  fetch('/upvote', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id1, userid: user._id }),
  })
    .then((res) => res.json())
    .then((data) => {
      const voteCount = document.getElementById("vc/" + id1);
      voteCount.innerHTML = "Votes : " + (data.votes);
      color(data.status, id1)
      add_verified(data.votes);
    })
    .catch((err) => {
      console.error(err);
    });
}

function downclick(id) {
  const id1 = id.split("/")[1];
  fetch('/downvote', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id1, userid: user._id }),
  })
    .then((res) => res.json())
    .then((data) => {
      const voteCount = document.getElementById("vc/" + id1);
      voteCount.innerHTML = "Votes : " + (data.votes);
      color(data.status, id1)
      add_verified(data.votes);
    })
    .catch((err) => {
      console.error(err);
    });
}
