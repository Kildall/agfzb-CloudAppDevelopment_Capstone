
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');


async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      const db = 'dealerships'
      cloudant.setServiceUrl(params.COUCH_URL);
      let documents = {};
      try {
        if(params.state){
            console.log('Query por estado')
            documents = await cloudant.postFind({
                db: db,
                selector: {
                    "st": {
                       "$eq": params.state
                    }
                 }
            });
            return {"documents": documents.result.docs};
        } else {
            console.log('Query sin estado')
            documents = await cloudant.postAllDocs({
                db: db,
                includeDocs: true,
                });
            return {"documents": documents.result};
        }
        
      } catch (error) {
          return { error: error.description };
      }
}