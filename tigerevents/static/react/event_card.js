'use strict';
const e = React.createElement;

class EventCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    return (
      <div class="card">
          <div class="card-body">
              <div class="row">
                  <div class="col-1">
                      <img class="article-img" src={imgurl} alt=""></img>
                  </div>
                  <div class="col">
                      xnxgnxnxdfnx<h3><a class="card-title" href={eventurl}>{ vent.title }</a></h3>
                  </div>
                  <div class="col-sm-auto">
                      <a class="btn btn-primary btn-sm mt-1 mb-1"
                          href="{{ url_for('events.save', event_id=event.id) }}">Save</a>
                      
                      <a class="btn btn-primary btn-sm mt-1 mb-1"
                          href="{{ url_for('events.rsvp', event_id=event.id) }}">Add to Calendar</a>
                  </div>
              </div>
              
              <div class="row">
                  <div class="col-xl-auto">
                      <div class="btn-group" role="group">
                          <button type="button" class="btn btn-light">{vent.host.name}</button>
                          <button type="button" class="btn btn-light">{vent.location}</button>
                          <button type="button" class="btn btn-light">{vent.start_date.strftime("%a %b %-d, %I:%M%p")} - {vent.end_date.strftime("%I:%M%p")}</button>
                        </div>
                  </div>
              </div>

              <p class="card-text">{ vent.description }</p>
          </div>
      </div>
    );
  }
}

const domContainer = document.querySelector('#event_card');
console.log("test");
ReactDOM.render(e(EventCard), domContainer);