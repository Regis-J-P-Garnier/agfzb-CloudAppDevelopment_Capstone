function main(params) {
    if (!("rows" in params)){return {error:500};};
    returnData = params.rows.map((row) => { return {
          id: row.doc.id,
          city: row.doc.city,
          state: row.doc.state,
          st: row.doc.st,      
          address: row.doc.address,
          zip: row.doc.zip,
          lat: row.doc.lat,
          long: row.doc.long,
          short_name: row.doc.short_name,
          full_name: row.doc.full_name
          }});
    if (returnData.length==0){return {error:404};}
    else
        {return {data:returnData}};     
}
