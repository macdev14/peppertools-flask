const io = require("socket.io-client");
const { Manager } = require("socket.io-client");


const manager = new Manager("https://peppertools-test.herokuapp.com", {
  reconnectionDelayMax: 10000

});

const socket = manager.socket("/api/progress/", {
  reconnectionDelayMax: 10000,
  auth: {
    authorization: localStorage.getItem('auth')
  },
  query: {
    "n_os": "8430"
  }
});

console.log(socket)

