using { sap.common } from '@sap/cds/common';

service ChatService {
    @readonly entity ChatResponse {
        key id   : UUID;
        query    : String;
        response : String;
    }

    function askLLM(query: String) returns ChatResponse;
}
