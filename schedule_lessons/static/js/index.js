import React from 'react'
import ReactDOM from 'react-dom'

function Welcome(props) {
  return <h1>Hello shreyas ddddssssss, {props.name}</h1>;
}

const element = <Welcome name="nisarg" />;
ReactDOM.render(
  element,
  document.getElementById('react')
);