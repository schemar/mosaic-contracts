// Copyright 2018 OpenST Ltd.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// ----------------------------------------------------------------------------
//
// http://www.simpletoken.org/
//
// ----------------------------------------------------------------------------

const messageBusUtilsKlass = require('./messagebus_utils');
const messageBus = require('../../test_lib/message_bus.js');
const messageBusUtils = new messageBusUtilsKlass();

let MessageStatusEnum = messageBus.MessageStatusEnum;

contract('MessageBus.declareRevocationMessage()', async (accounts) => {
    let params;

    beforeEach(async function () {

        await messageBusUtils.deployedMessageBus();
        params = messageBusUtils.defaultParams(accounts);
    });

    it('should fail when message status is undeclared in outbox', async () => {
        let message = 'Message on source must be Declared.';
        params.message = message;

        await messageBusUtils.declareRevocationMessage(params, false);

    });

    it('should fail when message status is Progressed in outbox', async () => {
        let message = 'Message on source must be Declared.';
        params.message = message;

        await messageBusUtils.declareMessage(params, true);
        await messageBusUtils.progressOutbox(params, true);

        await messageBusUtils.declareRevocationMessage(params, false);

    });

    it('should fail when message status is DeclaredRevocation in outbox', async () => {
        let message = 'Message on source must be Declared.';
        params.message = message;

        await messageBusUtils.declareMessage(params, true);
        await messageBusUtils.declareRevocationMessage(params, true);

        await messageBusUtils.declareRevocationMessage(params, false);

    });

    it('should fail when message status is Revoked in outbox', async () => {
        let message = 'Message on source must be Declared.';
        params.message = message;

        await messageBusUtils.declareMessage(params, true);
        await messageBusUtils.declareRevocationMessage(params, true);
        params.messageStatus = MessageStatusEnum.Revoked;
        await messageBusUtils.progressOutboxRevocation(params, true);

        await messageBusUtils.declareRevocationMessage(params, false)

    });
});