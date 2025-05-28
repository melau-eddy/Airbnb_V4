$(document).ready(function () {
  const checkedAmenities = {};

  $('input[type="checkbox"]').change(function () {
    const amenityId = $(this).attr('data-id');
    const amenityName = $(this).attr('data-name');

    if (this.checked) {
      checkedAmenities[amenityId] = amenityName;
    } else {
      delete checkedAmenities[amenityId];
    }

    // Update the h4 inside the amenities div
    const amenityList = Object.values(checkedAmenities).join(', ');
    $('.amenities h4').text(amenityList);
  });

  $.get('http://0.0.0.0:5001/api/v1/status/', function (data) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
      console.log('Available off');
    }
  });
  $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    type: 'POST',
    data: JSON.stringify({}),
    contentType: 'application/json',
    success: function (data) {
      $.each(data, function (index, place) {
        const article = $('<article></article>');

        const title_box = $('<div></div>');
        const name = $('<h2></h2>').text(place.name);
        const price_by_night = $('<div></div>').text("$" + place.price_by_night);
        title_box.append(name, price_by_night);

        const information = $('<div></div>');
        const max_guest = $('<div></div>').text(place.max_guest + " Guests");
        const number_rooms = $('<div></div>').text(place.number_rooms + " Rooms");
        const number_bathrooms = $('<div></div>').text(place.number_bathrooms + " Bathrooms");
        information.append(max_guest, number_rooms, number_bathrooms);

        const urrl = 'http://0.0.0.0:5001/api/v1/users/' + place.user_id;
	let user = $('<div></div>');
        $.get(urrl, function (data) {
          user.html('<b>Owner:</b> ' + data.first_name + " " + data.last_name);
        });

        const description = $('<div></div>').text(place.description);

	title_box.addClass('title_box');
	price_by_night.addClass('price_by_night');
	information.addClass('information');
	max_guest.addClass('max_guest');
	number_rooms.addClass('number_rooms');
	number_bathrooms.addClass('number_bathrooms');
	user.addClass('user');
	description.addClass('description');

        article.append(title_box, information, user, description);

        $('.places').append(article);
      });
    }
  });
});
