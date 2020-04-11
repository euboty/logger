// Normally data transformations should be done in the database -> raspi too slow
// Then data transformations should be done in the backend at least -> raspi too slow
// worst case: Data transformation in the browser itself  ¯\_(ツ)_/¯

function getDateTimeString(timestamp) {
  const date = new Date(timestamp * 1000);
  return (
    (date.getMonth()+1).toString().padStart(2, "0") +
    "-" +
    date.getDate().toString().padStart(2, "0") +
    " " +
    date.getHours().toString().padStart(2, "0") +
    ":" +
    date.getMinutes().toString().padStart(2, "0")
  );
}

/**
 * Takes a dataset and options and aggregates the data in intervals.
 *
 * @param {Array} dataList Data from server [List of timestamps, List of data]
 * @param {number} windowSize Size of the window for aggregation
 * @param {string} aggregation One of "avg", "min".
 */
function groupAndAggregate({ dataList, windowSize, aggregation }) {
  const [timestamps, data] = dataList;
  const endTime = timestamps[timestamps.length - 1];

  // generate the windows to group by
  const windows = [];
  const aggregatedData = [];
  let dataIndex = 0;
  let valuesToAggregate = [];
  for (let window = timestamps[0]; window < endTime; window += windowSize) {
    // fill and aggregate all data in the window
    while (timestamps[dataIndex] < window + windowSize) {
      valuesToAggregate.push(data[dataIndex]);
      dataIndex += 1;
    }

    let result;
    if (valuesToAggregate.length === 0) {
      result = null;
    } else if (aggregation === "avg") {
      result = valuesToAggregate.reduce((p, c) => p + c, 0) / valuesToAggregate.length;
    } else if (aggregation === "min") {
      result = Math.min.apply(null, valuesToAggregate);
    } else {
      throw new Error(`Not implemented aggregation ${aggregation}`);
    }

    windows.push(getDateTimeString(window));
    aggregatedData.push(result);
    valuesToAggregate = [];
  }

  return [windows, aggregatedData];
}
