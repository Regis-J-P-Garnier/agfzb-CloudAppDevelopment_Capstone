function main(params) {
    if (!("docs" in params)){return {error:500};};
    returnData = params.docs.map((doc) => { return {
          id: doc.id,
          city: doc.city,
          state: doc.state,
          st: doc.st,      
          address: doc.address,
          zip: doc.zip,
          lat: doc.lat,
          long: doc.long,   
          short_name: doc.short_name,
          full_name: doc.full_name
          }});
    if (returnData.length==0){return {error:404};}
    else
        {return {data:returnData}};
}
